from fastapi import APIRouter, HTTPException, status, Depends

from schemas.users import ShowUser
from schemas.auth import Token
from services.auth import AuthService
from utils.security import encode_bearer_token, decode_bearer_token
from utils.dependencies import get_auth_service

auth_router = APIRouter()


@auth_router.post("/auth/login", response_model=Token)
async def login(email: str, password: str, auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = encode_bearer_token(email)
    return token


@auth_router.get("/auth/me", response_model=ShowUser)
async def get_me(user_data: dict = Depends(decode_bearer_token), auth_service: AuthService = Depends(get_auth_service)):
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found")
    email = user_data.get("email", None)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not found in token data")

    user = await auth_service.get_user_by_email_for_auth(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token, email not found")
    return user
