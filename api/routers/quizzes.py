from fastapi import APIRouter, Depends, HTTPException, Body, Path
from fastapi_pagination import Page, Params, paginate

from schemas.quizzes import *
from schemas.questions import *
from schemas.answers import *
from services.company import CompanyService
from services.quizzes import QuizService
from utils.dependencies import get_company_service, get_quiz_service
from api.routers.users import get_user_data

quiz_router = APIRouter()


# Route to create a new quiz
@quiz_router.post("/company/{company_id}/quiz", response_model=QuizResponse)
async def create_quiz(
        quiz_data: QuizCreate,
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service),
        quiz_service: QuizService = Depends(get_quiz_service),
):
    try:
        # Check if the user is the owner or admin of the company
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email,
                                                                                          quiz_data.company_id)

        # Create the quiz
        created_quiz = await quiz_service.create_quiz(user_email, quiz_data)
    except HTTPException as exc:
        raise exc

    return created_quiz


# Route to update an existing quiz
@quiz_router.put("/company/{company_id}/quiz/{quiz_id}", response_model=QuizResponse)
async def update_quiz(
        company_id: int = Path(...),
        quiz_id: int = Path(...),
        quiz_data: QuizUpdate = Body(),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service),
        quiz_service: QuizService = Depends(get_quiz_service),
):
    try:
        # Check if the user is the owner or admin of the company
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)

        # Update the quiz
        updated_quiz = await quiz_service.update_quiz(quiz_id, quiz_data)

    except HTTPException as exc:
        raise exc

    return updated_quiz


# Route get quiz
@quiz_router.get("/company/{company_id}/quiz/{quiz_id}", response_model=QuizResponse)
async def get_quiz_by_id(
        company_id: int = Path(...),
        quiz_id: int = Path(...),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service),
        quiz_service: QuizService = Depends(get_quiz_service),
):
    try:
        # Check if the user is the owner or admin of the company
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)

        # Retrieve the quiz by ID
        quiz = await quiz_service.get_quiz_by_quiz_id(quiz_id)
    except HTTPException as exc:
        raise exc

    return quiz


# Route to get a list of quizzes for a specific company
@quiz_router.get("/company/{company_id}/quizzes", response_model=Page[QuizResponse])
async def get_all_quizzes_by_company(
        company_id: int = Path(...),
        params: Params = Depends(),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service),
        quiz_service: QuizService = Depends(get_quiz_service),
):
    try:
        # Check if the user is the owner or admin of the company
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)

        # Retrieve quizzes by company ID
        quizzes = await quiz_service.get_all_quizzes()

    except HTTPException as exc:
        raise exc

    return paginate(quizzes, params)


# Route to delete an existing quiz
@quiz_router.delete("/company/{company_id}/quiz/{quiz_id}", response_model=QuizResponse)
async def delete_quiz(
        company_id: int = Path(...),
        quiz_id: int = Path(...),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service),
        quiz_service: QuizService = Depends(get_quiz_service),
):
    try:
        # Check if the user is the owner or admin of the company
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)

        # Delete the quiz
        deleted_quiz_id = await quiz_service.delete_quiz(quiz_id)
    except HTTPException as exc:
        raise exc

    return deleted_quiz_id


@quiz_router.put("/company/{company_id}/quizzes/question/{question_id}", response_model=QuestionResponse)
async def update_question(
        company_id: int = Path(...),
        question_id: int = Path(...),
        question_data: QuestionUpdate = Body(),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service),
        quiz_service: QuizService = Depends(get_quiz_service),
):
    try:
        # Check if the user is the owner or admin of the company
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)

        # Update the question
        updated_question = await quiz_service.update_question(question_id, question_data)

    except HTTPException as exc:
        raise exc

    return updated_question


@quiz_router.put("/company/{company_id}/quizzes/questions/answer/{answer_id}", response_model=AnswerResponse)
async def update_answer(
        company_id: int = Path(...),
        answer_id: int = Path(...),
        answer_data: AnswerUpdate = Body(),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service),
        quiz_service: QuizService = Depends(get_quiz_service),
):
    try:
        # Check if the user is the owner or admin of the company
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)

        # Update the question
        updated_answer = await quiz_service.update_answer(answer_id, answer_data)

    except HTTPException as exc:
        raise exc

    return updated_answer


@quiz_router.get("/company/{company_id}/quiz/{quiz_id}/questions/", response_model=Page[QuestionResponse])
async def get_all_question_by_quiz_id(
        company_id: int = Path(...),
        quiz_id: int = Path(...),
        params: Params = Depends(),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service),
        quiz_service: QuizService = Depends(get_quiz_service),
):
    try:
        # Check if the user is the owner or admin of the company
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)

        # Retrieve quizzes by company ID
        quizzes = await quiz_service.get_all_questions(quiz_id)

    except HTTPException as exc:
        raise exc

    return paginate(quizzes, params)

@quiz_router.get("/company/{company_id}/quizzes/question/{question_id}/", response_model=Page[AnswerResponse])
async def get_all_answers_by_question_id(
        company_id: int = Path(...),
        question_id: int = Path(...),
        params: Params = Depends(),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service),
        quiz_service: QuizService = Depends(get_quiz_service),
):
    try:
        # Check if the user is the owner or admin of the company
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)

        # Retrieve quizzes by company ID
        quizzes = await quiz_service.get_all_answer(question_id)

    except HTTPException as exc:
        raise exc

    return paginate(quizzes, params)


@quiz_router.post("/company/{company_id}/quiz/{quiz_id}/question/{question_id}/user_answer/", response_model=UserAnswersResponse)
async def create_user_answer(
        company_id: int,
        user_answer_data: UserAnswersCreate = Body(),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service),
        quiz_service: QuizService = Depends(get_quiz_service),
):
    try:
        # Check if the user is a member of the company
        await company_service.check_user_in_company_by_email(company_id, user_email)

        # Create the user answer
        created_user_answer = await quiz_service.create_user_answer(user_email, user_answer_data)

    except HTTPException as exc:
        raise exc

    return created_user_answer


@quiz_router.post("/companies/quizzes/result/", response_model=List[QuizResultResponse])
async def create_quiz_result(
        quiz_result_data: QuizResultCreate = Body(),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service),
        quiz_service: QuizService = Depends(get_quiz_service),
):
    try:
        # Create the quiz result
        created_quiz_result = await quiz_service.create_quiz_result(quiz_result_data)

    except HTTPException as exc:
        raise exc

    return created_quiz_result
