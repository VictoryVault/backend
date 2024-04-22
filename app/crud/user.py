from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserCreate


async def create(db: AsyncSession, data: UserCreate) -> User | None:
    id = uuid4().hex

    transaction = User(id=id, **data.model_dump())
    try:
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
    except Exception:
        await db.rollback()
        return None

    return transaction


async def get(db: AsyncSession, id: str) -> User | None:
    try:
        transaction = await db.get(User, id)
    except NoResultFound:
        return None
    return transaction


async def get_all(db: AsyncSession) -> list[User]:
    return (await db.execute(select(User))).scalars().all()
