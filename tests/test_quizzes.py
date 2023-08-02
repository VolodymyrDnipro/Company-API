import pytest
from fastapi import status
from httpx import AsyncClient
import config
from jose import jwt

@pytest.mark.runafter("test_company_change_user_role_in_company")
@pytest.mark.asyncio
async def test_create_quiz(ac: AsyncClient):
    quiz_data = {
        "company_id": 1,
        "name": "first quiz",
        "description": "bla bla bla bla",
        "frequency_in_days": 2,
        "is_active": "true",
        "questions": [{
            "question_text": "first question_text",
            "is_active": "true",
            "answers": [{
                "answer_text": "first answer_text",
                "is_correct": "true"
            },
                {
                    "answer_text": "second answer_text",
                    "is_correct": "false"
                },
                {
                    "answer_text": "third answer_text",
                    "is_correct": "false"
                }
            ]
        },
            {
                "question_text": "second question_text",
                "is_active": "true",
                "answers": [{
                    "answer_text": "first answer_text",
                    "is_correct": "true"
                },
                    {
                        "answer_text": "second answer_text",
                        "is_correct": "false"
                    },
                    {
                        "answer_text": "third answer_text",
                        "is_correct": "false"
                    }
                ]
            }
        ]
    }

    quiz_data2 = {
        "company_id": 4,
        "name": "first quiz",
        "description": "bla bla bla bla",
        "frequency_in_days": 2,
        "is_active": "true",
        "questions": [{
            "question_text": "first question_text",
            "is_active": "true",
            "answers": [{
                "answer_text": "first answer_text",
                "is_correct": "true"
            },
                {
                    "answer_text": "second answer_text",
                    "is_correct": "false"
                },
                {
                    "answer_text": "third answer_text",
                    "is_correct": "false"
                }
            ]
        },
            {
                "question_text": "second question_text",
                "is_active": "true",
                "answers": [{
                    "answer_text": "first answer_text",
                    "is_correct": "true"
                },
                    {
                        "answer_text": "second answer_text",
                        "is_correct": "false"
                    },
                    {
                        "answer_text": "third answer_text",
                        "is_correct": "false"
                    }
                ]
            }
        ]
    }

    email = "testemail2@example.com"  # user_id = 2
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    response = await ac.post("/company/1/quiz", json=quiz_data, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200

    data = response.json()
    assert "quiz_id" in data
    assert "company_id" in data
    assert "name" in data
    assert "description" in data
    assert "frequency_in_days" in data
    assert "is_active" in data
    await ac.post("/company/4/quiz", json=quiz_data2, headers={"Authorization": f"Bearer {token}"})


@pytest.mark.asyncio
async def test_update_quiz(ac: AsyncClient):
    company_id = 1
    quiz_id = 1
    quiz_data = {
        "name": "Updated Quiz Name",
        "description": "Updated description",
        "frequency_in_days": 2,
        "is_active": True
    }

    email = "testemail2@example.com"  # user_id = 2
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    response = await ac.put(f"/company/{company_id}/quiz/{quiz_id}", json=quiz_data,
                            headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200

    data = response.json()
    assert "quiz_id" in data
    assert "company_id" in data
    assert "name" in data
    assert "description" in data
    assert "frequency_in_days" in data
    assert "is_active" in data


@pytest.mark.asyncio
async def test_get_quiz_by_id(ac: AsyncClient):
    company_id = 1
    quiz_id = 1
    email = "testemail2@example.com"  # user_id = 2
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    response = await ac.get(f"/company/{company_id}/quiz/{quiz_id}", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert "quiz_id" in data
    assert "company_id" in data
    assert "author_id" in data
    assert "name" in data
    assert "description" in data
    assert "frequency_in_days" in data
    assert "is_active" in data


@pytest.mark.asyncio
async def test_get_all_quizzes_by_company(ac: AsyncClient):
    company_id = 1
    email = "testemail2@example.com"  # user_id = 2
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    response = await ac.get(f"/company/{company_id}/quizzes", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0



@pytest.mark.asyncio
async def test_delete_quiz(ac: AsyncClient):
    company_id = 1
    quiz_id = 1

    email = "testemail2@example.com"  # user_id = 2
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    response = await ac.delete(f"/company/{company_id}/quiz/{quiz_id}", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200

    data = response.json()
    assert "quiz_id" in data
    assert "company_id" in data
    assert "author_id" in data
    assert "name" in data
    assert "description" in data
    assert "frequency_in_days" in data
    assert "is_active" in data


@pytest.mark.asyncio
async def test_update_question(ac: AsyncClient):
    company_id = 1
    question_id = 1
    question_data = {
        "question_text": "Updated Quiz Name",
        "is_active": True
    }

    email = "testemail2@example.com"  # user_id = 2
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    response = await ac.put(f"/company/{company_id}/quizzes/question/{question_id}", json=question_data,
                            headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200

    data = response.json()
    assert "question_id" in data
    assert "quiz_id" in data
    assert "question_text" in data
    assert "is_active" in data


@pytest.mark.asyncio
async def test_update_answer(ac: AsyncClient):
    company_id = 1
    answer_id = 1
    answer_data = {
        "answer_text": "Updated answer text",
        "is_correct": True
    }

    email = "testemail2@example.com"  # user_id = 2
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    response = await ac.put(f"/company/{company_id}/quizzes/questions/answer/{answer_id}", json=answer_data,
                            headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200

    data = response.json()
    assert "answer_id" in data
    assert "question_id" in data
    assert "answer_text" in data
    assert "is_correct" in data


@pytest.mark.asyncio
async def test_get_all_question_by_quiz_id(ac: AsyncClient):
    company_id = 1
    quiz_id = 1
    email = "testemail2@example.com"  # user_id = 2
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    response = await ac.get(f"/company/{company_id}/quiz/{quiz_id}/questions/",
                                headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0


@pytest.mark.asyncio
async def test_get_all_answers_by_question_id(ac: AsyncClient):
    company_id = 4
    question_id = 3
    email = "testemail2@example.com"
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    response = await ac.get(f"/company/{company_id}/quizzes/question/{question_id}/",
                            headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0



@pytest.mark.asyncio
async def test_create_user_answer(ac: AsyncClient):
    company_id = 4
    user_answer_data = {
        "quiz_id": 2,
        "question_id": 3,
        "answer_id": 7
    }
    email = "testemail4@example.com"
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    response = await ac.post(f"/company/{company_id}/quiz/2/question/3/user_answer/",
                             json=user_answer_data,
                             headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200

    data = response.json()
    assert "user_answer_id" in data
    assert "user_id" in data
    assert "quiz_id" in data
    assert "question_id" in data
    assert "answer_id" in data


@pytest.mark.runafter("test_create_user_answer")
@pytest.mark.asyncio
async def test_create_quiz_result(ac: AsyncClient):
    quiz_result_data = {
        "user_id": 4
    }

    email = "testemail2@example.com"
    token_data = {"email": email}
    token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    response = await ac.post("/companies/quizzes/result/",
                             json=quiz_result_data,
                             headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0
