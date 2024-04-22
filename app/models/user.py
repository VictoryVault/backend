from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint

from app.models.util import TimestampModel, UUIDModel


class UserBase(SQLModel):
    email: str = Field(max_length=255, nullable=False)
    full_name: str = Field(max_length=255, nullable=False)


class User(UUIDModel, TimestampModel, UserBase, table=True):
    __tablename__ = "Users"
    __table_args__ = (UniqueConstraint("email"),)


class UserRead(UUIDModel, UserBase): ...


class UserCreate(UserBase): ...
