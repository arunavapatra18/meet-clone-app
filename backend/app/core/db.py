from typing import Annotated
from fastapi import Depends
from sqlalchemy import MetaData
from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings


engine = create_engine(str(settings.POSTGRES_DB_URI), echo=True)


def init_db():
    """Initialize DB with all tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get DB session

    Yields:
        Session: DB session
    """
    with Session(engine) as session:
        yield session


db_session_dependency = Annotated[Session, Depends(get_session)]
