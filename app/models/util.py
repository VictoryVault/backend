import uuid as uuid_pkg
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import text
from sqlmodel import Field, SQLModel


class HealthCheck(BaseModel):
    name: str
    version: str
    description: str


class StatusMessage(BaseModel):
    status: bool
    message: str


# SQLModel Mixin to automatically add primary key id configuration to a table
class UUIDModel(SQLModel):
    uuid: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True},
    )

# SQLModel Mixin to automatically add timestamp configuration and creation to a table
# timestamps are generated based on server time and record the time of entry creation
# as well as automatically add last update timestamp
class TimestampModel(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_column_kwargs={"server_default": text("current_timestamp(0)")},
    )

    updated_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("current_timestamp(0)"),
            "onupdate": text("current_timestamp(0)"),
        },
    )
