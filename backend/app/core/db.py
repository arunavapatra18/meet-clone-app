from sqlalchemy import MetaData
from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings


engine = create_engine(str(settings.POSTGRES_DB_URI), echo=True)

custom_metadata = MetaData(naming_convention=settings.POSTGRES_INDEXES_NAMING_CONVENTION)

SQLModel.metadata = custom_metadata

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
