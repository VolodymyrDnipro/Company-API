from db.session import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import ShowUser, ShowAllUsers, UserCreate, DeleteUserResponse, UpdatedUserResponse, UpdateUserRequest
from services.users import UsersService
from fastapi import HTTPException

users_router = APIRouter()

users_service = UsersService()


@users_router.get("/users/", response_model=ShowAllUsers)
async def get_all_users(session: AsyncSession = Depends(get_session)):
    users = await users_service.get_all_users(session)
    if users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return {"users": users}


@users_router.get("/user/{user_id}", response_model=ShowUser)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await users_service.get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@users_router.post("/user/", response_model=ShowUser)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    created_user = await users_service.create_user(user, session)
    return created_user


@users_router.put("/user/{user_id}", response_model=UpdatedUserResponse)
async def update_user(user_id: int, user: UpdateUserRequest, session: AsyncSession = Depends(get_session)):
    updated_user = await users_service.update_user(user_id, user, session)
    return {"updated_user_id": updated_user.user_id}


@users_router.delete("/user/{user_id}", response_model=DeleteUserResponse)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    await users_service.delete_user(user_id, session)
    return {"deleted_user_id": user_id}
