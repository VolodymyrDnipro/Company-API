import pytest
from httpx import AsyncClient
import config
from jose import jwt


@pytest.mark.asyncio
async def test_user_get_active_notifications(ac: AsyncClient):
    email = "testemail4@example.com"  # user_id = 4
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    response = await ac.get("/notifications/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0


@pytest.mark.asyncio
async def test_user_get_active_notifications(ac: AsyncClient):
    email = "testemail4@example.com"  # user_id = 4
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    notification_id = 1

    response = await ac.put(f"/notifications/{notification_id}/read/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert "notification_id" in data
    assert "user_id" in data
    assert "timestamp" in data
    assert "status" in data
    assert "text" in data
