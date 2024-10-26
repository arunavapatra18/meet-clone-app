from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: EmailStr


class User(UserBase, table=True):
    id: UUID | None = Field(primary_key=True, default_factory=uuid4)
    disabled: bool | None
    name: str | None
    password: str


class UserRegister(UserBase):
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class RegisterResponse(BaseModel):
    message: str
    user_id: UUID


class TokenData(BaseModel):
    user_id: str
