from fastapi import APIRouter, HTTPException, status, Depends, Body
from pydantic import EmailStr

from schemas.users import ShowUser
from schemas.auth import Token
from services.auth import AuthService
from utils.security import encode_bearer_token
from utils.dependencies import get_auth_service
from api.routers.users import get_user_data

auth_router = APIRouter()


@auth_router.post("/auth/login", response_model=Token)
async def login(email: EmailStr = Body(...), password: str = Body(...), auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = encode_bearer_token(email)
    return token


@auth_router.get("/auth/me", response_model=ShowUser)
async def get_me(user_email: str = Depends(get_user_data), auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.get_user_by_email_for_auth(user_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token, email not found")
    return user
