import jwt

from datetime import datetime, timedelta, timezone
from typing import Union
from passlib.context import CryptContext

from app.core.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """Create a new access token

    Args:
        data (dict): data to encode
        expires_delta (Union[timedelta, None], optional): Expiry time. Defaults to None.

    Returns:
        str: Access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def generate_password_hash(password_str: str):
    """Generate hashed password

    Args:
        password_str (str): Plaintext password

    Returns:
        str: Hashed password
    """
    return password_context.hash(password_str)


def verify_password(password_str: str, hashed_password: str):
    """Verify password input

    Args:
        password_str (str): Plaintext password
        hashed_password (str): Hashed password in DB

    Returns:
        bool: True if matched, else False
    """
    return password_context.verify(password_str, hashed_password)
