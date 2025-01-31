from pydantic import EmailStr
from sqlmodel import Session, select

from app.models import User


def get_user_by_email(session: Session, email: EmailStr):
    """Get user from DB with input email

    Args:
        session (Session): DB Session
        email (EmailStr): Input email

    Returns:
        User/None: User with the email, else None
    """
    query = select(User).where(User.email == email)
    return session.exec(query).first()


def get_user_by_id(session: Session, id: str):
    """Get user from DB with input id

    Args:
        session (Session): DB Session
        id (str): Input id

    Returns:
        User/None: User with the id, else None
    """
    query = select(User).where(User.id == id)
    return session.exec(query).first()
