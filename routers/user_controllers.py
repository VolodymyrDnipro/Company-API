from db.session import get_session
from db.models import User
from managers.user_manager import CRUDBase
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import ShowUser, ShowAllUsers, UserCreate, DeleteUserResponse, UpdatedUserResponse, UpdateUserRequest
from hashing import Hasher
user_router = APIRouter()

session = get_session()

@user_router.get("/users", response_model=ShowAllUsers)
async def get_all_users(session: AsyncSession = Depends(get_session)):
    async with session.begin():
        user_crud = CRUDBase[User](User, session)
        users = await user_crud.get_all()
        return {"users": users}


@user_router.get("/users/{user_id}", response_model=ShowUser)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        user_crud = CRUDBase[User](User, session)
        user = await user_crud.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

@user_router.post("/users", response_model=ShowUser)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        user_crud = CRUDBase[User](User, session)
        user_obj = User(name=user.name, surname=user.surname, email=user.email, hashed_password=Hasher.get_password_hash(user.password))
        created_user = await user_crud.create(user_obj)
        return created_user


@user_router.put("/users/{user_id}", response_model=UpdatedUserResponse)
async def update_user(user_id: int, user: UpdateUserRequest, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        user_crud = CRUDBase[User](User, session)
        existing_user = await user_crud.get_by_id(user_id)
        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        updated_user = await user_crud.update(existing_user, user.dict())
        return {"updated_user_id": updated_user.user_id}


@user_router.delete("/users/{user_id}", response_model=DeleteUserResponse)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        user_crud = CRUDBase[User](User, session)
        existing_user = await user_crud.get_by_id(user_id)
        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        await user_crud.delete(existing_user)
        return {"deleted_user_id": user_id}
