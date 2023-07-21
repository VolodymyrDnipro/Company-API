from db.session import get_session
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import ShowUser
from schemas.auth import Token
from services.auth import AuthService
from utils.security import encode_bearer_token, decode_bearer_token

auth_router = APIRouter()
auth_service = AuthService()


@auth_router.post("/auth/login", response_model=Token)
async def login(email: str, password: str, session: AsyncSession = Depends(get_session)):
    user = await auth_service.authenticate_user(email, password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = encode_bearer_token(email)
    return token


@auth_router.get("/auth/me", response_model=ShowUser)
async def get_me(user_data: dict = Depends(decode_bearer_token), session: AsyncSession = Depends(get_session),):
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found")

    email = user_data.get("email", None)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not found in token data")

    user = await auth_service.get_user_by_email_for_auth(email, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token, email not found")
    return user
