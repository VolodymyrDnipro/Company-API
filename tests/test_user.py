import pytest
from fastapi import status
from httpx import AsyncClient
from fastapi.security import HTTPAuthorizationCredentials
import config
from jose import jwt
from utils.security import decode_bearer_token, encode_bearer_token


@pytest.mark.first
@pytest.mark.asyncio
async def test_create_user(ac: AsyncClient):
    user_data_firs = {
        "name": "testname",
        "surname": "testsurname",
        "email": "testemail@example.com",
        "password": "string",
    }

    user_data_second = {
        "name": "testname",
        "surname": "testsurname",
        "email": "testemail2@example.com",
        "password": "string",
    }
    user_data_third = {
        "name": "testname",
        "surname": "testsurname",
        "email": "testemail3@example.com",
        "password": "string",
    }
    user_data_fourth = {
        "name": "testname",
        "surname": "testsurname",
        "email": "testemail4@example.com",
        "password": "string",
    }
    user_data_fifth = {
        "name": "testname",
        "surname": "testsurname",
        "email": "testemail5@example.com",
        "password": "string",
    }

    response_first = await ac.post("/user/", json=user_data_firs)
    assert response_first.status_code == status.HTTP_200_OK

    data_first = response_first.json()
    assert "user_id" in data_first
    assert data_first["name"] == user_data_firs["name"]
    assert data_first["surname"] == user_data_firs["surname"]
    assert data_first["email"] == user_data_firs["email"]

    response_second = await ac.post("/user/", json=user_data_second)
    assert response_second.status_code == status.HTTP_200_OK

    response_third = await ac.post("/user/", json=user_data_third)
    assert response_third.status_code == status.HTTP_200_OK

    response_fourth = await ac.post("/user/", json=user_data_fourth)
    assert response_fourth.status_code == status.HTTP_200_OK

    response_fifth = await ac.post("/user/", json=user_data_fifth)
    assert response_fifth.status_code == status.HTTP_200_OK


# Test for route  /auth/login
async def test_login(ac: AsyncClient):
    login_data = {
        "email": "testemail@example.com",
        "password": "string",
    }
    response = await ac.post("/auth/login", json=login_data)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "access_token" in data

    global ACCESS_TOKEN
    ACCESS_TOKEN = data["access_token"]

    credentials = HTTPAuthorizationCredentials(scheme="bearer", credentials=data["access_token"])
    decoded_token_data = decode_bearer_token(credentials)

    assert decoded_token_data["email"] == login_data["email"]


# Test for route /auth/me
@pytest.mark.asyncio
async def test_get_me(ac: AsyncClient):
    email = "testemail@example.com"
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    response = await ac.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "user_id" in data
    assert data["email"] == email


# Test for receiving a user by his ID
@pytest.mark.asyncio
async def test_get_user_by_id(ac: AsyncClient):
    user_id = 1

    response = await ac.get(f"/user/{user_id}", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "user_id" in data
    assert data["user_id"] == user_id
    assert data["name"] == "testname"
    assert data["surname"] == "testsurname"
    assert data["email"] == "testemail@example.com"


# Test to receive all users
@pytest.mark.asyncio
async def test_get_all_users(ac: AsyncClient):
    response = await ac.get("/users/", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0


@pytest.mark.asyncio
async def test_update_user(ac: AsyncClient):
    user_id = 1
    user_update_data = {
        "name": "updname",
        "surname": "updsurname",
        "password": "updpassword",
    }

    response = await ac.put(f"/user/{user_id}", json=user_update_data,
                            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "updated_user_id" in data
    assert data["updated_user_id"] == user_id


@pytest.mark.asyncio
async def test_deactivate_user(ac: AsyncClient):
    user_id = 1

    response = await ac.delete(f"/user/{user_id}", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "deactivated_user" in data
    assert data["deactivated_user"] == user_id
