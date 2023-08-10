from db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from services.users import UsersService
from services.auth import AuthService
from services.company import CompanyService
from services.quizzes import QuizService
from services.analytics import AnalyticsService
from services.notifications import NotificationsService


def get_users_service(session: AsyncSession = Depends(get_session)) -> UsersService:
    return UsersService(session)


def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(session)


def get_company_service(session: AsyncSession = Depends(get_session)) -> CompanyService:
    return CompanyService(session)


def get_quiz_service(session: AsyncSession = Depends(get_session)) -> QuizService:
    return QuizService(session)


def get_analytics_service(session: AsyncSession = Depends(get_session)) -> AnalyticsService:
    return AnalyticsService(session)


def get_notifications_service(session: AsyncSession = Depends(get_session)) -> NotificationsService:
    return NotificationsService(session)


