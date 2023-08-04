from typing import List

from fastapi import APIRouter, Depends, HTTPException, Body, Path, Response, Query
from fastapi_pagination import Page, Params, paginate
from fastapi.responses import FileResponse
from datetime import date

from schemas.questions import QuestionUpdate
from schemas.answers import AnswerUpdate
from services.company import CompanyService
from services.users import UsersService
from services.quizzes import QuizService
from services.analytics import AnalyticsService
from utils.dependencies import get_company_service, get_quiz_service, get_analytics_service, get_users_service
from api.routers.users import get_user_data

analytics_router = APIRouter()


@analytics_router.get("/analytics/rating/", response_model=int)
async def user_gets_average_rating_about_himself(
        user_email: str = Depends(get_user_data),
        analytics_service: AnalyticsService = Depends(get_analytics_service),
):
    try:
        user_rating = await analytics_service.get_self_rating(user_email)
    except HTTPException as exc:
        raise exc
    return user_rating


@analytics_router.get("/analytics/rating/quizzes", response_model=List[dict])
async def get_user_rating_by_all_quizzes_by_date(
        start_date: date = Query(...),
        end_date: date = Query(...),
        user_email: str = Depends(get_user_data),
        analytics_service: AnalyticsService = Depends(get_analytics_service),
):
    try:
        user_rating = await analytics_service.get_user_rating_by_all_quizzes_by_date(user_email, start_date, end_date)
    except HTTPException as exc:
        raise exc
    return user_rating


@analytics_router.get("/analytics/quizzes/last_completed", response_model=List[dict])
async def get_quizzes_and_last_completion_time(
        user_email: str = Depends(get_user_data),
        analytics_service: AnalyticsService = Depends(get_analytics_service),
):
    try:
        quiz_completion_times = await analytics_service.get_quizzes_and_last_completion_time(user_email)
    except HTTPException as exc:
        raise exc
    return quiz_completion_times


# # # Company Analytics # # #
@analytics_router.get("/analytics/rating/company/{company_id}", response_model=List[dict])
async def company_get_average_scores(
        company_id: int = Path(),
        start_date: date = Query(...),
        end_date: date = Query(...),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service),
        analytics_service: AnalyticsService = Depends(get_analytics_service),
):
    try:
        # Check if the user is the owner or admin of the company
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)

        user_rating = await analytics_service.company_get_average_scores(company_id, start_date, end_date)
    except HTTPException as exc:
        raise exc
    return user_rating


@analytics_router.get("/analytics/rating/company/{company_id}/user/{user_id}/quizzes", response_model=List[dict])
async def company_get_average_scores_by_all_users(
        company_id: int = Path(),
        user_id: int = Path(),
        start_date: date = Query(...),
        end_date: date = Query(...),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service),
        analytics_service: AnalyticsService = Depends(get_analytics_service),
):
    try:
        # Check if the user is the owner or admin of the company
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)

        user_rating = await analytics_service.company_get_average_scores_by_all_users(user_id, company_id, start_date, end_date)
    except HTTPException as exc:
        raise exc
    return user_rating


@analytics_router.get("/analytics/rating/company/{company_id}/users", response_model=List[dict])
async def company_get_all_users_and_last_completion_time(
        company_id: int = Path(),
        user_email: str = Depends(get_user_data),
        company_service: CompanyService = Depends(get_company_service),
        analytics_service: AnalyticsService = Depends(get_analytics_service),
):
    try:
        # Check if the user is the owner or admin of the company
        await company_service.check_who_this_user_in_company_admin_or_owner_by_company_id(user_email, company_id)

        users_completion_times = await analytics_service.company_get_all_users_and_last_completion_time(company_id)
    except HTTPException as exc:
        raise exc
    return users_completion_times