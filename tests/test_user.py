import pytest
from fastapi import status
from httpx import AsyncClient
from fastapi.security import HTTPAuthorizationCredentials
import config
from jose import jwt
from utils.security import decode_bearer_token, encode_bearer_token


# Тест на створення користувача
@pytest.mark.first
@pytest.mark.asyncio
async def test_create_user(ac: AsyncClient):
    # Створюємо дані для 1 користувача
    user_data_firs = {
        "name": "testname",
        "surname": "testsurname",
        "email": "testemail@example.com",
        "password": "string",
    }

    # Створюємо дані для 2 користувача
    user_data_second = {
        "name": "testname",
        "surname": "testsurname",
        "email": "testemail2@example.com",
        "password": "string",
    }
    # Створюємо дані для 3 користувача
    user_data_third = {
        "name": "testname",
        "surname": "testsurname",
        "email": "testemail3@example.com",
        "password": "string",
    }
    # Створюємо дані для 4 користувача
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

    # Відправляємо POST-запит для створення користувача
    response_first = await ac.post("/user/", json=user_data_firs)

    # Перевіряємо, чи запити були успішними (статус 200)
    assert response_first.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про створеного користувача
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



# Тест для роуту /auth/login
async def test_login(ac: AsyncClient):
    # Створюємо дані для входу
    login_data = {
        "email": "testemail@example.com",
        "password": "string",
    }
    # Відправляємо POST-запит для входу
    response = await ac.post("/auth/login", json=login_data)

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернувся токен доступу
    data = response.json()
    assert "access_token" in data

    # Зберігаємо токен для використання в інших тестах
    global ACCESS_TOKEN
    ACCESS_TOKEN = data["access_token"]

    # Декодуємо токен
    credentials = HTTPAuthorizationCredentials(scheme="bearer", credentials=data["access_token"])
    decoded_token_data = decode_bearer_token(credentials)

    # Перевіряємо, чи є очікувані дані в декодованому токені
    assert decoded_token_data["email"] == login_data["email"]


# Тест для роуту /auth/me
@pytest.mark.asyncio
async def test_get_me(ac: AsyncClient):
    # Створюємо дані для створення токена
    email = "testemail@example.com"
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    # Відправляємо GET-запит для отримання даних користувача
    response = await ac.get("/auth/me", headers={"Authorization": f"Bearer {token}"})

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про користувача
    data = response.json()
    assert "user_id" in data
    assert data["email"] == email


# Тест на отримання користувача за його ID
@pytest.mark.asyncio
async def test_get_user_by_id(ac: AsyncClient):
    user_id = 1

    # Відправляємо GET-запит для отримання користувача за його ID
    response = await ac.get(f"/user/{user_id}", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про користувача за його ID
    data = response.json()
    assert "user_id" in data
    assert data["user_id"] == user_id
    assert data["name"] == "testname"
    assert data["surname"] == "testsurname"
    assert data["email"] == "testemail@example.com"



# Тест на отримання всіх користувачів
@pytest.mark.asyncio
async def test_get_all_users(ac: AsyncClient):
    # Відправляємо GET-запит для отримання всіх користувачів
    response = await ac.get("/users/", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про всіх користувачів
    data = response.json()
    assert "items" in data  # Перевіряємо наявність ключа "items"
    assert isinstance(data["items"], list)  # Перевіряємо, що значення по ключу "items" є списком
    assert len(data["items"]) > 0  # Перевіряємо, що список користувачів не є порожнім


# Тест на оновлення користувача
@pytest.mark.asyncio
async def test_update_user(ac: AsyncClient):
    # Створюємо дані для оновлення користувача
    user_id = 1
    user_update_data = {
        "name": "updname",
        "surname": "updsurname",
        "password": "updpassword",
    }

    # Відправляємо PUT-запит для оновлення користувача з переданим токеном доступу
    response = await ac.put(f"/user/{user_id}", json=user_update_data, headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про оновленого користувача
    data = response.json()
    assert "updated_user_id" in data
    assert data["updated_user_id"] == user_id


# Тест для деактивації користувача
@pytest.mark.asyncio
async def test_deactivate_user(ac: AsyncClient):
    # Підготовка даних для запиту
    user_id = 1

    # Відправляємо DELETE-запит для деактивації користувача
    response = await ac.delete(f"/user/{user_id}", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про деактивованого користувача
    data = response.json()
    assert "deactivated_user" in data
    assert data["deactivated_user"] == user_id

