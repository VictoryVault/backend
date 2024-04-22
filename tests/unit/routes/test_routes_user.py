import pytest
from pytest import MonkeyPatch
from httpx import AsyncClient
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import user


@pytest.mark.asyncio
async def test_get(client: AsyncClient, monkeypatch: MonkeyPatch):
    test_response_payload = {
        "email": "string",
        "full_name": "string",
        "uuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    }

    async def mock_get(id: UUID4, db: AsyncSession):
        return test_response_payload

    monkeypatch.setattr(user, "get", mock_get)

    response = await client.get(
        "/api/user/get-user?id=3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )
    assert response.status_code == 200
    assert response.json() == test_response_payload


@pytest.mark.asyncio
async def test_get_not_present(client: AsyncClient, monkeypatch: MonkeyPatch):
    test_response_payload = None

    async def mock_get(id: UUID4, db: AsyncSession):
        return test_response_payload

    monkeypatch.setattr(user, "get", mock_get)

    response = await client.get(
        "/api/user/get-user?id=3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )
    assert response.status_code == 200
    assert response.json() == test_response_payload
