from typing import List

from fastapi import APIRouter, Depends, HTTPException, Body, Path, Response
from fastapi_pagination import Page, Params, paginate
from fastapi.responses import FileResponse

from schemas.notifications import NotificationResponse
from schemas.questions import QuestionUpdate
from schemas.answers import AnswerUpdate
from services.company import CompanyService
from services.quizzes import QuizService
from services.notifications import NotificationsService
from utils.dependencies import get_company_service, get_quiz_service, get_notifications_service
from api.routers.users import get_user_data

notifications_router = APIRouter()


# Route to create a new quiz
@notifications_router.get("/notifications/", response_model=List[NotificationResponse])
async def user_get_active_notifications(
        user_email: str = Depends(get_user_data),
        notification_service: NotificationsService = Depends(get_notifications_service),
):
    try:
        notifications = await notification_service.user_get_active_notifications_by_email(user_email)
    except HTTPException as exc:
        raise exc
    return notifications


@notifications_router.put("/notifications/{notification_id}/read/", response_model=NotificationResponse)
async def user_mark_notification_as_read(
        notification_id: int,
        user_email: str = Depends(get_user_data),
        notification_service: NotificationsService = Depends(get_notifications_service),
):
    try:
        notification = await notification_service.user_mark_notification_as_read(user_email, notification_id)
    except HTTPException as exc:
        raise exc
    return notification
