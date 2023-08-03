from fastapi import APIRouter, Depends, HTTPException, Body, Path, Response
from fastapi_pagination import Page, Params, paginate
from fastapi.responses import FileResponse

from schemas.quizzes import *
from schemas.questions import *
from schemas.answers import *
from services.company import CompanyService
from services.quizzes import QuizService
from services.analytics import AnalyticsService
from utils.dependencies import get_company_service, get_quiz_service, get_analytics_service
from api.routers.users import get_user_data

analytics_router = APIRouter()


# Route to create a new quiz
@analytics_router.get("/analytics/rating", response_model=UserRatingResponse)
async def get_user_rating(
        user_id: int,
        user_email: str = Depends(get_user_data),
        quiz_service: QuizService = Depends(get_quiz_service),
        company_service: CompanyService = Depends(get_company_service),
        analytics_service: AnalyticsService = Depends(get_analytics_service),
):
    try:
        user_rating = await user_service.get_user_rating(user_id)
    except HTTPException as exc:
        raise exc
    return user_rating