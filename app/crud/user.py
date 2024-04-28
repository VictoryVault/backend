from uuid import uuid4 # python library for creating UUIDs

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserCreate


async def create(db: AsyncSession, data: UserCreate) -> User | None:
    # generate random UUID for new DB entry
    user_id = uuid4().hex

    # unpack the UserCreate object to create User, which during creation 
    # will also populate with the timestamp due to mixin
    transaction = User(id=user_id, **data.model_dump())
    try:
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
    except Exception:
        await db.rollback()
        return None

    return transaction


async def get(db: AsyncSession, user_id: str) -> User | None:
    try:
        # User type is associated with table, so gets from that table
        transaction = await db.get(User, user_id)
    except NoResultFound:
        return None
    return transaction


async def get_all(db: AsyncSession) -> list[User]:
    # User type is associated with table, so gets from that table
    return (await db.execute(select(User))).scalars().all()
