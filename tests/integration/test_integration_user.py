import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_user(client: AsyncClient):
    response = await client.get("/api/user/get-users")

    assert response.status_code == 200
    assert len(response.json()) == 0

    response = await client.post(
        "/api/user/create-user",
        json={"email": "test@example.com", "full_name": "Full Name Test"},
    )

    assert response.status_code == 200

    response = await client.get("/api/user/get-users")

    assert response.status_code == 200
    assert len(response.json()) == 1
    
    id = (response.json()[0])["uuid"]

    response = await client.get(f"/api/user/get-user?id={id}")

    assert response.status_code == 200
    assert response.json()["full_name"] == "Full Name Test"
    assert response.json()["email"] == "test@example.com"
