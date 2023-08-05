from datetime import date

import pytest
from fastapi import status
from httpx import AsyncClient
import config
from jose import jwt


@pytest.mark.asyncio
async def test_user_gets_average_rating_about_himself(ac: AsyncClient):
    email = "testemail4@example.com"  # user_id = 4
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    response = await ac.get("/analytics/rating/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response == int


@pytest.mark.asyncio
async def test_get_user_rating_by_all_quizzes_by_date(ac: AsyncClient):
    start_date = date(2022, 2, 2)
    end_date = date(2024, 2, 2)

    email = "testemail4@example.com"  # user_id = 4
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    response = await ac.get(f"/analytics/rating/quizzes?start_date={start_date}&end_date={end_date}",
                            headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0


@pytest.mark.asyncio
async def test_get_quizzes_and_last_completion_time(ac: AsyncClient):
    email = "testemail4@example.com"  # user_id = 4
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    response = await ac.get("/analytics/quizzes/last_completed", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0


@pytest.mark.asyncio
async def test_company_get_average_scores(ac: AsyncClient):
    email = "testemail2@example.com"  # user_id = 2
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    company_id = 4
    start_date = date(2022, 2, 2)
    end_date = date(2024, 2, 2)

    response = await ac.get(f"/analytics/rating/company/{company_id}/?start_date={start_date}&end_date={end_date}",
                            headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0


@pytest.mark.asyncio
async def test_company_get_average_scores_by_user_id(ac: AsyncClient):
    email = "testemail2@example.com"  # user_id = 2
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    company_id = 4
    user_id = 2
    start_date = date(2022, 2, 2)
    end_date = date(2024, 2, 2)

    response = await ac.get(
        f"/analytics/rating/company/{company_id}/user/{user_id}/quizzes/?start_date={start_date}&end_date={end_date}",
        headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0


@pytest.mark.asyncio
async def test_company_get_all_users_and_last_completion_time(ac: AsyncClient):
    email = "testemail2@example.com"  # user_id = 2
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    company_id = 4

    response = await ac.get(
        f"/analytics/rating/company/{company_id}/users/",headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0

