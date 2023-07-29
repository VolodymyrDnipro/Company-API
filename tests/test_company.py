import pytest
from fastapi import status
from httpx import AsyncClient
import config
from jose import jwt

# Тест на створення компанії
@pytest.mark.asyncio
async def test_create_company(ac: AsyncClient):
    # Створюємо дані для створення токена
    email = "testemail2@example.com"
    token_data = {"email": email}
    global ACCESS_TOKEN
    ACCESS_TOKEN = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    # Моделюємо дані з токеном авторизації
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    # Підготовка даних для запиту
    company_data_first = {
        "name": "First Test Company",
        "description": "First Test Description",
        "visibility": "visible_to_all",
        "owner_id": 2
    }

    company_data_second = {
        "name": "Second Test Company",
        "description": "Second Test Description",
        "visibility": "visible_to_all",
        "owner_id": 2
    }
    company_data_third = {
        "name": "Third Test Company",
        "description": "Third Test Description",
        "visibility": "visible_to_all",
        "owner_id": 2
    }
    company_data_fourth = {
        "name": "Third Test Company",
        "description": "Third Test Description",
        "visibility": "visible_to_all",
        "owner_id": 2
    }

    # Відправляємо POST-запит для створення 1 компанії
    response_first = await ac.post("/company/", json=company_data_first, headers=headers)

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response_first.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про створену компанію
    data_first = response_first.json()
    assert "company_id" in data_first
    assert "name" in data_first
    assert "description" in data_first
    assert "owner_id" in data_first
    assert data_first["name"] == company_data_first["name"]
    assert data_first["description"] == company_data_first["description"]
    assert data_first["visibility"] == company_data_first["visibility"]

    # Відправляємо POST-запит для створення 2 компанії
    response_second = await ac.post("/company/", json=company_data_second, headers=headers)
    # Перевіряємо, чи запит був успішним (статус 200)
    assert response_second.status_code == status.HTTP_200_OK

    # Відправляємо POST-запит для створення 3 компанії
    response_third = await ac.post("/company/", json=company_data_third, headers=headers)
    # Перевіряємо, чи запит був успішним (статус 200)
    assert response_third.status_code == status.HTTP_200_OK

    # Відправляємо POST-запит для створення 4 компанії
    response_fourth = await ac.post("/company/", json=company_data_fourth, headers=headers)
    # Перевіряємо, чи запит був успішним (статус 200)
    assert response_fourth.status_code == status.HTTP_200_OK


# Тест для роуту /companies/
@pytest.mark.asyncio
async def test_get_companies(ac: AsyncClient):
    # Відправляємо GET-запит для отримання всіх компаній
    response = await ac.get("/companies/", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про компанії
    data = response.json()
    assert "items" in data  # Перевіряємо наявність ключа "items"
    assert isinstance(data["items"], list)  # Перевіряємо, що значення по ключу "items" є списком
    assert len(data["items"]) > 0  # Перевіряємо, що список компаній не є порожнім

    # Перевіряємо, чи відповідь містить пагінацію
    assert "page" in data
    assert "pages" in data
    assert "size" in data


# Тест для роуту /company/{company_id}/
@pytest.mark.asyncio
async def test_get_company(ac: AsyncClient):
    company_id = 1

    # Відправляємо GET-запит для отримання компанії за її ID
    response = await ac.get(f"/company/{company_id}/", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про компанію за її ID
    data = response.json()
    assert "company_id" in data
    assert "name" in data
    assert "description" in data
    assert "owner_id" in data
    assert "visibility" in data


# Тест для роуту /company/{company_id}/
@pytest.mark.asyncio
async def test_update_company(ac: AsyncClient):
    company_id = 1
    updated_company_data = {
        "name": "Updated Company Name",
        "description": "Updated Description",
        "visibility": "hidden",
        "is_active": False
    }

    # Виконуємо PUT-запит для оновлення компанії
    response = await ac.put(f"/company/{company_id}/", json=updated_company_data, headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про оновлену компанію
    data = response.json()
    assert "updated_company_id" in data
    assert data["updated_company_id"] == company_id


# Тест для роуту /deactivate_company/{company_id}/
@pytest.mark.asyncio
async def test_deactivate_company(ac: AsyncClient):
    # Підготовка даних для тесту
    company_id = 1

    # Виконуємо PUT-запит для деактивації компанії за її ID
    response = await ac.delete(f"/deactivate_company/{company_id}/", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про деактивовану компанію
    data = response.json()
    assert "updated_company_id" in data
    assert data["updated_company_id"] == company_id


# Тест для роуту /company/{company_id}/request/{user_id}
@pytest.mark.asyncio
async def test_create_request_to_user_from_company(ac: AsyncClient):
    company_id = 2
    user_id_3 = 3   # "testemail3@example.com"
    user_id_4 = 4   # "testemail4@example.com"
    user_id_5 = 5   # "testemail5@example.com"
    # Виконуємо POST-запит для створення запиту
    response1 = await ac.post(f"/company/{company_id}/request/{user_id_3}", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response1.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про створений запит
    data = response1.json()
    assert "request_id" in data
    assert "user_id" in data
    assert "company_id" in data
    assert "status" in data

    response2 = await ac.post(f"/company/{company_id}/request/{user_id_4}",
                             headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
    assert response2.status_code == status.HTTP_200_OK
    response3 = await ac.post(f"/company/{company_id}/request/{user_id_5}",
                              headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
    assert response3.status_code == status.HTTP_200_OK


# Тест для роуту /company/request/{request_id}/cancel/
@pytest.mark.asyncio
async def test_company_cancel_request_to_user(ac: AsyncClient):
    # Підготовка даних для запиту
    request_id = 3

    # Відправляємо PUT-запит для скасування запиту
    response = await ac.put(f"/company/request/{request_id}/cancel/", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про скасований запит
    data = response.json()
    assert "deactivated_request_id" in data
    assert data["deactivated_request_id"] == request_id


# Тест для /company_requests_from_company/{company_id}
@pytest.mark.asyncio
async def test_company_get_all_requests_from_company_to_users(ac: AsyncClient):
    # Підготовка даних для запиту
    company_id = 2

    # Відправляємо GET-запит для отримання всіх запитів з компанії до користувачів зі статусом PENDING
    response = await ac.get(f"/company_requests_from_company/{company_id}", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про запити
    data = response.json()
    assert "items" in data  # Перевіряємо наявність ключа "items"
    assert isinstance(data["items"], list)  # Перевіряємо, що значення по ключу "items" є списком
    assert len(data["items"]) > 0  # Перевіряємо, що список запитів не є порожнім

    # Перевіряємо, чи відповідь містить пагінацію
    assert "page" in data
    assert "pages" in data
    assert "size" in data


# Тест для створення запиту користувачем до компанії
@pytest.mark.asyncio
async def test_user_create_request_to_company(ac: AsyncClient):
    # Створюємо дані для створення токена
    email = "testemail3@example.com" # user_id = 3
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    # Підготовка даних для запиту
    company_id_3 = 3
    company_id_4 = 4

    # Відправляємо POST-запит для створення запиту користувачем до компанії
    response = await ac.post(f"/user/{company_id_3}/request/", headers={"Authorization": f"Bearer {token}"})

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про створений запит
    data = response.json()
    assert "request_id" in data
    assert "user_id" in data
    assert "company_id" in data
    assert "status" in data

    await ac.post(f"/user/{company_id_4}/request/", headers={"Authorization": f"Bearer {token}"})


# Тест для скасування запиту користувачем до компанії
@pytest.mark.asyncio
async def test_user_cancel_request_to_company(ac: AsyncClient):
    # Створюємо дані для створення токена
    email = "testemail3@example.com"
    token_data = {"email": email}
    access_token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    # Моделюємо дані з токеном авторизації
    headers = {"Authorization": f"Bearer {access_token}"}

    # Підготовка даних для запиту
    request_id = 5

    # Відправляємо PUT-запит для скасування запиту користувачем до компанії
    response = await ac.put(f"/user/request/{request_id}/cancel/", headers=headers)

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про скасований запит
    data = response.json()
    assert "request_id" in data
    assert "user_id" in data
    assert "company_id" in data
    assert "status" in data


# Тест для оновлення статусу запиту користувача до компанії
@pytest.mark.asyncio
async def test_user_update_company_request_status(ac: AsyncClient):
    # Створюємо дані для створення токена
    email = "testemail3@example.com"
    token_data = {"email": email}
    access_token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    # Моделюємо дані з токеном авторизації
    headers = {"Authorization": f"Bearer {access_token}"}

    # Підготовка даних для запиту
    request_data = {
        "request_id": 1,
        "status": "accepted"  # або "declined" залежно від того, який статус хочемо задати
    }
    request_id = 1

    # Відправляємо PUT-запит для оновлення статусу запиту користувача до компанії
    response = await ac.put(f"/user/request/{request_id}/status/", json=request_data, headers=headers)

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про оновлений запит
    data = response.json()
    assert "updated_request_id" in data
    assert "status" in data
    assert data["updated_request_id"] == request_data["request_id"]
    assert data["status"] == request_data["status"]


# Тест для роута /user_requests/
@pytest.mark.asyncio
async def test_get_user_requests(ac: AsyncClient):
    # Створюємо дані для створення токена
    email = "testemail4@example.com"
    token_data = {"email": email}
    access_token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    # Моделюємо дані з токеном авторизації
    headers = {"Authorization": f"Bearer {access_token}"}

    # Виконуємо GET-запит для отримання реквестів користувача
    response = await ac.get("/user_requests/", headers=headers)

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про реквести
    data = response.json()
    assert "items" in data  # Перевіряємо наявність ключа "items"
    assert isinstance(data["items"], list)  # Перевіряємо, що значення по ключу "items" є списком
    assert len(data["items"]) > 0  # Перевіряємо, що список  не є порожнім


# Тест для роута /user_created_requests/
@pytest.mark.asyncio
async def test_get_user_created_requests(ac: AsyncClient):
    # Створюємо дані для створення токена
    email = "testemail3@example.com"
    token_data = {"email": email}
    access_token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    # Моделюємо дані з токеном авторизації
    headers = {"Authorization": f"Bearer {access_token}"}

    # Виконуємо GET-запит для отримання реквестів, створених користувачем
    response = await ac.get("/user_created_requests/", headers=headers)

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про реквести, які були створені користувачем
    data = response.json()
    assert "items" in data  # Перевіряємо наявність ключа "items"
    assert isinstance(data["items"], list)  # Перевіряємо, що значення по ключу "items" є списком
    assert len(data["items"]) > 0  # Перевіряємо, що список  не є порожнім


# Тест для роута /users_leave_company/{company_id}
@pytest.mark.asyncio
async def test_user_leave_company(ac: AsyncClient):
    # Створюємо дані для створення токена
    email = "testemail3@example.com"
    token_data = {"email": email}
    access_token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    # Моделюємо дані з токеном авторизації
    headers = {"Authorization": f"Bearer {access_token}"}

    company_id = 2

    # Создаем данные для запроса, где is_active=False, что означает, что пользователь покидает компанию
    request_data = {"is_active": False}

    # Виконуємо PUT-запит для выхода пользователя из компании
    response = await ac.put(f"/users_leave_company/{company_id}", json=request_data, headers=headers)

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про компанію і статус is_active
    data = response.json()
    assert "company_id" in data
    assert "is_active" in data
    assert data["company_id"] == company_id
    assert data["is_active"] is False


# Тест для роута /company_request/{request_id}/
@pytest.mark.asyncio
async def test_company_update_user_request(ac: AsyncClient):
    request_id = 4

    # Создаем данные для запроса, где status=RequestStatus.ACCEPTED, что означает, что запрос будет принят
    request_data = {"request_id": request_id, "status": "accepted"}

    # Виконуємо PUT-запит для обновления запроса
    response = await ac.put(f"/company_request/{request_id}/", json=request_data, headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про обновлений запит
    data = response.json()
    assert "updated_request_id" in data
    assert "status" in data
    assert data["updated_request_id"] == request_id
    assert data["status"] == "accepted"


# Тест для роута /company_get_all_users/{company_id}
@pytest.mark.asyncio
async def test_get_all_users_in_company(ac: AsyncClient):
    company_id = 3

    # Виконуємо GET-запит для отримання списку всіх користувачів в компанії
    response = await ac.get(f"/company_get_all_users/{company_id}", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про користувачів в компанії
    data = response.json()
    assert "items" in data  # Перевіряємо наявність ключа "items"
    assert isinstance(data["items"], list)  # Перевіряємо, що значення по ключу "items" є списком
    assert len(data["items"]) > 0  # Перевіряємо, що список  не є порожнім


# Тест для роуту /company_deactivate_user_in_company/{company_id}
@pytest.mark.asyncio
async def test_company_deactivate_user_in_company(ac: AsyncClient):
    company_id = 3
    user_id = 3
    is_active = False

    # Спробуємо деактивувати користувача в компанії
    response = await ac.put(f"/company_deactivate_user_in_company/{company_id}",
                            json={"user_id": user_id, "is_active": is_active},
                            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    # Перевіряємо, чи запит був успішним (статус 200)
    assert response.status_code == status.HTTP_200_OK

    # Перевіряємо, чи повернулися правильні дані про деактивацію користувача
    data = response.json()
    assert "user_id" in data
    assert "is_active" in data

    # Перевіряємо, чи дані про деактивацію користувача відповідають переданим даним
    assert data["user_id"] == user_id
    assert data["is_active"] == is_active
