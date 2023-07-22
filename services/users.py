from fastapi import HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.users import User
from utils.hashing import Hasher
from managers.user_manager import CRUDBase
from schemas.users import UserCreate, UpdateUserRequest


class UsersService:
    def __init__(self, session: AsyncSession):
        self.user_crud = CRUDBase[User](User, session)

    async def get_all_users(self) -> List[User]:
        return await self.user_crud.get_all()

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.user_crud.get_by_field(user_id, field_name='user_id')
        return user

    async def create_user(self, user_data: UserCreate) -> User:
        hashed_password = Hasher.get_password_hash(user_data.password)
        user = User(name=user_data.name, surname=user_data.surname, email=user_data.email,
                    hashed_password=hashed_password)
        created_user = await self.user_crud.create(user)
        return created_user

    async def update_user(self, user_id: int, user_data: UpdateUserRequest) -> User:
        existing_user = await self.user_crud.get_by_field(user_id, field_name='user_id')
        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        updated_user = await self.user_crud.update(existing_user, user_data.dict())
        return updated_user

    async def delete_user(self, user_id: int) -> None:
        existing_user = await self.user_crud.get_by_field(user_id, field_name='user_id')
        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        deleted_user = await self.user_crud.delete(existing_user)
        return deleted_user

    async def check_user_before_update(self, user_id: int, user_data: UpdateUserRequest, email: str) -> User:
        user = await self.user_crud.get_by_field(user_id, field_name='user_id')
        if user.email == email:
            raise HTTPException(status_code=403, detail="Forbidden to update")

        updated_user = await self.update_user(user_id, user_data)
        return updated_user

    async def check_user_before_delete(self, user_id: int, email: str) -> None:
        user = await self.user_crud.get_by_field(user_id, field_name='user_id')
        if user.email == email:
            raise HTTPException(status_code=403, detail="Forbidden to delete")

        deleted_user = await self.delete_user(user_id)
        return deleted_user

