from db.session import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import ShowUser, ShowAllUsers, UserCreate, DeleteUserResponse, UpdatedUserResponse, UpdateUserRequest
from services.users import UsersService

user_router = APIRouter()
session = get_session()


@user_router.get("/users", response_model=ShowAllUsers)
async def get_all_users(session: AsyncSession = Depends(get_session)):
    async with session.begin():
        users_service = UsersService(session)
        users = await users_service.get_all_users()
        return {"users": users}


@user_router.get("/users/{user_id}", response_model=ShowUser)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        users_service = UsersService(session)
        user = await users_service.get_user_by_id(user_id)
        return user


@user_router.post("/users", response_model=ShowUser)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        users_service = UsersService(session)
        created_user = await users_service.create_user(user)
        return created_user


@user_router.put("/users/{user_id}", response_model=UpdatedUserResponse)
async def update_user(user_id: int, user: UpdateUserRequest, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        users_service = UsersService(session)
        updated_user = await users_service.update_user(user_id, user)
        return {"updated_user_id": updated_user.user_id}


@user_router.delete("/users/{user_id}", response_model=DeleteUserResponse)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        users_service = UsersService(session)
        await users_service.delete_user(user_id)
        return {"deleted_user_id": user_id}
