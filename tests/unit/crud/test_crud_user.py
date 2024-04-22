import pytest

from app.crud.user import get_all
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_get_all(db_session: AsyncSession):
    users = await get_all(db_session)
    assert len(users) == 0
