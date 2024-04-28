from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint

from app.models.util import TimestampModel, UUIDModel


class UserBase(SQLModel):
    email: str = Field(max_length=255, nullable=False)
    full_name: str = Field(max_length=255, nullable=False)


# Database table definition & Pydantic type courtesy of SQLModel inheritance
# Must be explicitly labelled as a table to be used by SQLAlchemy
# Uses mixins to automatically handle definition for an ID primary key
# and time of creation timestamp
class User(UUIDModel, TimestampModel, UserBase, table=True):
    __tablename__ = "Users"
    __table_args__ = (UniqueConstraint("email"),)
    hashed_password: str


# Used for type enforcement/declaration at interface
class UserRead(UUIDModel, UserBase): ...


# Used for type enforcement/declaration at interface
class UserCreate(UserBase): ...
