from datetime import datetime, timedelta, timezone

import jwt

from config import SECRET_KEY


# JWT configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


def create_access_token(customer_id: int) -> str:
    """Create a short-lived JWT for an authenticated customer."""

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(customer_id),
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_access_token(token: str) -> dict:
    """Verify a JWT and return its payload."""

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    return payload