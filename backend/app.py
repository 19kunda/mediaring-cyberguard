from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import SessionLocal, engine, Base
from models import Customer
from schemas import (
    CustomerCreate,
    CustomerUpdate,
    CustomerRegister,
    CustomerLogin,
    CustomerResponse,
)

from security import hash_password, verify_password
from auth import create_access_token, verify_access_token

app = FastAPI(title="MediaRing CyberGuard")
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH"],
    allow_headers=["Content-Type", "Authorization"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Configure Bearer token authentication.
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_customer(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    # Reject requests without an access token.
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify the JWT access token.
    try:
        payload = verify_access_token(credentials.credentials)
        customer_id = int(payload.get("sub", ""))

    except (InvalidTokenError, TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Find the customer associated with the token.
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    # Reject missing, inactive or unconfigured accounts.
    if (
        customer is None
        or not customer.is_active
        or not customer.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid or inactive customer account.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return customer


@app.get("/")
def home():
    return {"message": "MediaRing CyberGuard API is running!"}

@app.post(
    "/auth/register",
    response_model=CustomerResponse,
    status_code=201,
)
def register_customer(
    customer_data: CustomerRegister,
    db: Session = Depends(get_db),
):
    # Check whether the email address is already registered.
    existing_customer = db.query(Customer).filter(
        Customer.email == customer_data.email
    ).first()

    if existing_customer:
        raise HTTPException(
            status_code=409,
            detail="A customer with this email address already exists.",
        )

    # Hash the password before storing it.
    hashed_password = hash_password(customer_data.password)

    # Create the new customer account.
    new_customer = Customer(
        company_name=customer_data.company_name,
        email=customer_data.email,
        password_hash=hashed_password,
    )

    db.add(new_customer)

    try:
        db.commit()
        db.refresh(new_customer)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A customer with this email address already exists.",
        )

    return new_customer


@app.post("/auth/login")
def login_customer(
    login_data: CustomerLogin,
    db: Session = Depends(get_db),
):
    # Find the customer using their email address.
    customer = db.query(Customer).filter(
        Customer.email == login_data.email
    ).first()

    # Reject invalid email/password combinations.
    if (
        customer is None
        or not customer.password_hash
        or not verify_password(
            login_data.password,
            customer.password_hash,
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check whether the account is active.
    if not customer.is_active:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate a JWT access token.
    access_token = create_access_token(customer.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "customer": CustomerResponse.model_validate(customer),
    }
@app.get(
    "/auth/me",
    response_model=CustomerResponse,
)
def get_my_account(
    current_customer: Customer = Depends(get_current_customer),
):
    return current_customer

@app.put(
    "/auth/me",
    response_model=CustomerResponse,
)
def update_my_account(
    customer_data: CustomerUpdate,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    # Update only the authenticated customer's details.
    current_customer.company_name = customer_data.company_name
    current_customer.email = customer_data.email

    try:
        db.commit()
        db.refresh(current_customer)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A customer with this email address already exists.",
        )

    return current_customer
