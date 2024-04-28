import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_user(client: AsyncClient):
    # check there are no users when test starts
    response = await client.get("/api/users/")

    assert response.status_code == 200
    assert len(response.json()) == 0

    # create a user
    response = await client.post(
        "/api/users/",
        json={"email": "test@example.com", "full_name": "Full Name Test"},
    )

    assert response.status_code == 200

    # check that number of users is now 1
    response = await client.get("/api/users/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    
    id = (response.json()[0])["uuid"]

    # test GET on specific user created above
    response = await client.get(f"/api/users/{id}")

    assert response.status_code == 200
    assert response.json()["full_name"] == "Full Name Test"
    assert response.json()["email"] == "test@example.com"
