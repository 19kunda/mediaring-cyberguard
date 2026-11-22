from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import SessionLocal, engine, Base
from models import Customer
from schemas import CustomerCreate, CustomerUpdate

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
    allow_headers=["Content-Type"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "MediaRing CyberGuard API is running!"}


@app.post(
    "/customers",
    responses={
        409: {
            "description": "A customer with this email address already exists."
        }
    }
)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    existing_customer = db.query(Customer).filter(
        Customer.email == customer.email
    ).first()

    if existing_customer:
        raise HTTPException(
            status_code=409,
            detail="A customer with this email address already exists."
        )

    new_customer = Customer(
        company_name=customer.company_name,
        email=customer.email
    )

    db.add(new_customer)

    try:
        db.commit()
        db.refresh(new_customer)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A customer with this email address already exists."
        )

    return {
        "id": new_customer.id,
        "company_name": new_customer.company_name,
        "email": new_customer.email,
        "is_active": new_customer.is_active
    }
@app.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return customers


@app.get(
    "/customers/{customer_id}",
    responses={
        404: {
            "description": "Customer not found."
        }
    }
)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    return customer


@app.put(
    "/customers/{customer_id}",
    responses={
        404: {
            "description": "Customer not found."
        },
        409: {
            "description": "A customer with this email address already exists."
        }
    }
)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    existing_customer = db.query(Customer).filter(
        Customer.email == customer_data.email,
        Customer.id != customer_id
    ).first()

    if existing_customer:
        raise HTTPException(
            status_code=409,
            detail="A customer with this email address already exists."
        )

    customer.company_name = customer_data.company_name
    customer.email = customer_data.email

    try:
        db.commit()
        db.refresh(customer)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A customer with this email address already exists."
        )

    return {
        "id": customer.id,
        "company_name": customer.company_name,
        "email": customer.email,
        "is_active": customer.is_active
    }

@app.patch(
    "/customers/{customer_id}/deactivate",
    responses={
        404: {
            "description": "Customer not found."
        }
    }
)
def deactivate_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    customer.is_active = False

    db.commit()
    db.refresh(customer)

    return {
        "message": "Customer account deactivated successfully.",
        "id": customer.id,
        "company_name": customer.company_name,
        "email": customer.email,
        "is_active": customer.is_active
    }

@app.patch(
    "/customers/{customer_id}/reactivate",
    responses={
        404: {
            "description": "Customer not found."
        }
    }
)
def reactivate_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    customer.is_active = True

    db.commit()
    db.refresh(customer)

    return {
        "message": "Customer account reactivated successfully.",
        "id": customer.id,
        "company_name": customer.company_name,
        "email": customer.email,
        "is_active": customer.is_active
    }
