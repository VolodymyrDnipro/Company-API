import pytest
from fastapi import status
from httpx import AsyncClient
import config
from jose import jwt


# Test for the creation of a company
@pytest.mark.runafter("test_create_user")
@pytest.mark.asyncio
async def test_create_company(ac: AsyncClient):
    email = "testemail2@example.com"
    token_data = {"email": email}
    global ACCESS_TOKEN
    ACCESS_TOKEN = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

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

    response_first = await ac.post("/company/", json=company_data_first, headers=headers)

    assert response_first.status_code == status.HTTP_200_OK

    data_first = response_first.json()
    assert "company_id" in data_first
    assert "name" in data_first
    assert "description" in data_first
    assert "owner_id" in data_first
    assert data_first["name"] == company_data_first["name"]
    assert data_first["description"] == company_data_first["description"]
    assert data_first["visibility"] == company_data_first["visibility"]

    response_second = await ac.post("/company/", json=company_data_second, headers=headers)
    assert response_second.status_code == status.HTTP_200_OK

    response_third = await ac.post("/company/", json=company_data_third, headers=headers)
    assert response_third.status_code == status.HTTP_200_OK

    response_fourth = await ac.post("/company/", json=company_data_fourth, headers=headers)
    assert response_fourth.status_code == status.HTTP_200_OK


# Test for route /companies/
@pytest.mark.asyncio
async def test_get_companies(ac: AsyncClient):
    response = await ac.get("/companies/", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0

    assert "page" in data
    assert "pages" in data
    assert "size" in data


# Test for route /company/{company_id}/
@pytest.mark.asyncio
async def test_get_company(ac: AsyncClient):
    company_id = 1

    response = await ac.get(f"/company/{company_id}/", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "company_id" in data
    assert "name" in data
    assert "description" in data
    assert "owner_id" in data
    assert "visibility" in data


# Test for route /company/{company_id}/
@pytest.mark.asyncio
async def test_update_company(ac: AsyncClient):
    company_id = 1
    updated_company_data = {
        "name": "Updated Company Name",
        "description": "Updated Description",
        "visibility": "hidden",
        "is_active": False
    }

    response = await ac.put(f"/company/{company_id}/", json=updated_company_data,
                            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "updated_company_id" in data
    assert data["updated_company_id"] == company_id


# Test for route /deactivate_company/{company_id}/
@pytest.mark.asyncio
async def test_deactivate_company(ac: AsyncClient):
    company_id = 1

    response = await ac.delete(f"/deactivate_company/{company_id}/",
                               headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "updated_company_id" in data
    assert data["updated_company_id"] == company_id


# Test for route /company/{company_id}/request/{user_id}
@pytest.mark.runafter("test_create_company")
@pytest.mark.asyncio
async def test_create_request_to_user_from_company(ac: AsyncClient):
    company_id2 = 2
    company_id4 = 4
    user_id_3 = 3  # "testemail3@example.com"
    user_id_4 = 4  # "testemail4@example.com"
    user_id_5 = 5  # "testemail5@example.com"

    response1 = await ac.post(f"/company/{company_id2}/request/{user_id_3}",
                              headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    assert response1.status_code == status.HTTP_200_OK

    data = response1.json()
    assert "request_id" in data
    assert "user_id" in data
    assert "company_id" in data
    assert "status" in data

    response2 = await ac.post(f"/company/{company_id2}/request/{user_id_4}",
                              headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
    assert response2.status_code == status.HTTP_200_OK
    response3 = await ac.post(f"/company/{company_id2}/request/{user_id_5}",
                              headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
    assert response3.status_code == status.HTTP_200_OK

    response5 = await ac.post(f"/company/{company_id4}/request/{user_id_4}",
                              headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
    assert response5.status_code == status.HTTP_200_OK
    response6 = await ac.post(f"/company/{company_id4}/request/{user_id_5}",
                              headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
    assert response6.status_code == status.HTTP_200_OK


# Test for route /company/request/{request_id}/cancel/
@pytest.mark.asyncio
async def test_company_cancel_request_to_user(ac: AsyncClient):
    request_id = 3

    response = await ac.put(f"/company/request/{request_id}/cancel/",
                            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "deactivated_request_id" in data
    assert data["deactivated_request_id"] == request_id


# Test for route /company_requests_from_company/{company_id}
@pytest.mark.asyncio
async def test_company_get_all_requests_from_company_to_users(ac: AsyncClient):
    company_id = 2

    response = await ac.get(f"/company_requests_from_company/{company_id}",
                            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0

    assert "page" in data
    assert "pages" in data
    assert "size" in data


# Test for meeting with a friend to the company
@pytest.mark.asyncio
async def test_user_create_request_to_company(ac: AsyncClient):
    email = "testemail3@example.com"  # user_id = 3
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    company_id_3 = 3
    company_id_4 = 4

    response = await ac.post(f"/user/{company_id_3}/request/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "request_id" in data
    assert "user_id" in data
    assert "company_id" in data
    assert "status" in data

    await ac.post(f"/user/{company_id_4}/request/", headers={"Authorization": f"Bearer {token}"})


# Test for cancellation of a request by a user to a company
@pytest.mark.asyncio
async def test_user_cancel_request_to_company(ac: AsyncClient):
    email = "testemail3@example.com"
    token_data = {"email": email}
    access_token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    headers = {"Authorization": f"Bearer {access_token}"}

    request_id = 7

    response = await ac.put(f"/user/request/{request_id}/cancel/", headers=headers)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "request_id" in data
    assert "user_id" in data
    assert "company_id" in data
    assert "status" in data


# Test to update the status of the user's request to the company
@pytest.mark.runafter("test_create_request_to_user_from_company")
@pytest.mark.asyncio
async def test_user_update_company_request_status(ac: AsyncClient):
    email = "testemail3@example.com"
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    request_data = {
        "request_id": 1,
        "status": "accepted"
    }
    request_id = 1

    response = await ac.put(f"/user/request/{request_id}/status/", json=request_data,
                            headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "updated_request_id" in data
    assert "status" in data
    assert data["updated_request_id"] == request_data["request_id"]
    assert data["status"] == request_data["status"]

    email = "testemail4@example.com"
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)
    request_data = {
        "request_id": 4,
        "status": "accepted"
    }
    response = await ac.put(f"/user/request/{request_id}/status/", json=request_data,
                            headers={"Authorization": f"Bearer {token}"})

    email = "testemail5@example.com"
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)
    request_data = {
        "request_id": 5,
        "status": "accepted"
    }
    response = await ac.put(f"/user/request/{request_id}/status/", json=request_data,
                            headers={"Authorization": f"Bearer {token}"})


# Test for route /user_requests/
@pytest.mark.asyncio
async def test_get_user_requests(ac: AsyncClient):
    email = "testemail4@example.com"
    token_data = {"email": email}
    access_token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    headers = {"Authorization": f"Bearer {access_token}"}

    response = await ac.get("/user_requests/", headers=headers)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0


# Test for route /user_created_requests/
@pytest.mark.asyncio
async def test_get_user_created_requests(ac: AsyncClient):
    email = "testemail3@example.com"
    token_data = {"email": email}
    access_token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    headers = {"Authorization": f"Bearer {access_token}"}

    response = await ac.get("/user_created_requests/", headers=headers)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0


# Test for route /users_leave_company/{company_id}
@pytest.mark.asyncio
async def test_user_leave_company(ac: AsyncClient):
    email = "testemail3@example.com"
    token_data = {"email": email}
    access_token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    headers = {"Authorization": f"Bearer {access_token}"}

    company_id = 2

    request_data = {"is_active": False}

    response = await ac.put(f"/users_leave_company/{company_id}", json=request_data, headers=headers)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "company_id" in data
    assert "is_active" in data
    assert data["company_id"] == company_id
    assert data["is_active"] is False


# Test for route /company_request/{request_id}/
@pytest.mark.asyncio
async def test_company_update_user_request(ac: AsyncClient):
    request_id = 6
    request_data = {"request_id": request_id, "status": "accepted"}

    response = await ac.put(f"/company_request/{request_id}/", json=request_data,
                            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "updated_request_id" in data
    assert "status" in data
    assert data["updated_request_id"] == request_id
    assert data["status"] == "accepted"


# Test for route  /company_get_all_users/{company_id}
@pytest.mark.asyncio
async def test_get_all_users_in_company(ac: AsyncClient):
    company_id = 3

    response = await ac.get(f"/company_get_all_users/{company_id}", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0


# Test for route /company_deactivate_user_in_company/{company_id}
@pytest.mark.runafter("test_get_company_admins")
@pytest.mark.asyncio
async def test_company_deactivate_user_in_company(ac: AsyncClient):
    company_id = 4
    user_id = 5
    is_active = False

    response = await ac.put(f"/company_deactivate_user_in_company/{company_id}",
                            json={"user_id": user_id, "is_active": is_active},
                            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "user_id" in data
    assert "is_active" in data

    assert data["user_id"] == user_id
    assert data["is_active"] == is_active


# Test for route /company/{company_id}/changed_user/{user_id}
@pytest.mark.asyncio
async def test_company_change_user_role_in_company(ac: AsyncClient):
    company_id = 4
    user_id4 = 4
    user_id5 = 5
    new_role_type = "admin"

    response = await ac.put(f"/company/{company_id}/changed_user/{user_id4}",
                            json={"user_id": user_id4, "role_type": new_role_type},
                            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "user_id" in data
    assert "role_type" in data

    assert data["user_id"] == user_id4
    assert data["role_type"] == new_role_type

    await ac.put(f"/company/{company_id}/changed_user/{user_id5}",
                            json={"user_id": user_id5, "role_type": new_role_type},
                            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})


# Test for route /company/{company_id}/company_members/{role_type}
@pytest.mark.runafter("test_company_change_user_role_in_company")
@pytest.mark.asyncio
async def test_get_company_admins(ac: AsyncClient):
    company_id = 4
    role_type = "admin"

    response = await ac.get(f"/company/{company_id}/company_members/{role_type}",
                            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0
