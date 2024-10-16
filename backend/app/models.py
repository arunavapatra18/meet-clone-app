from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    name: str

class User(UserBase, table=True):
    id: UUID | None = Field(primary_key=True, default_factory=uuid4)