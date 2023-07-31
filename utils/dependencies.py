from db.session import get_session
from services.users import UsersService
from services.auth import AuthService
from services.company import CompanyService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


def get_users_service(session: AsyncSession = Depends(get_session)) -> UsersService:
    return UsersService(session)


def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(session)


def get_company_service(session: AsyncSession = Depends(get_session)) -> CompanyService:
    return CompanyService(session)