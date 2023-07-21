from typing import List
from db.models.users import User
from utils.hashing import Hasher
from managers.user_manager import CRUDBase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from schemas.users import UserCreate, UpdateUserRequest


class UsersService:
    async def get_all_users(self, session: AsyncSession) -> List[User]:
        user_crud = CRUDBase[User](User, session)
        return await user_crud.get_all()

    async def get_user_by_id(self, user_id: int, session: AsyncSession) -> User:
        user_crud = CRUDBase[User](User, session)
        user = await user_crud.get_by_field(user_id, field_name='user_id')
        return user

    async def create_user(self, user_data: UserCreate, session: AsyncSession) -> User:
        user_crud = CRUDBase[User](User, session)
        hashed_password = Hasher.get_password_hash(user_data.password)
        user = User(name=user_data.name, surname=user_data.surname, email=user_data.email,
                    hashed_password=hashed_password)
        created_user = await user_crud.create(user)
        return created_user

    async def update_user(self, user_id: int, user_data: UpdateUserRequest, session: AsyncSession) -> User:
        user_crud = CRUDBase[User](User, session)
        existing_user = await user_crud.get_by_field(user_id, field_name='user_id')
        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        updated_user = await user_crud.update(existing_user, user_data.dict())
        return updated_user

    async def delete_user(self, user_id: int, session: AsyncSession) -> None:
        user_crud = CRUDBase[User](User, session)
        existing_user = await user_crud.get_by_field(user_id, field_name='user_id')
        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        await user_crud.delete(existing_user)
