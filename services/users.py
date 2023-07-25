from fastapi import HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.models import User
from utils.hashing import Hasher
from managers.base_manager import CRUDBase
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

    async def update_user(self, user_id: int, user_data: UpdateUserRequest, email: str) -> User:
        current_user = await self.user_crud.get_by_field(email, field_name='email')
        user = await self.user_crud.get_by_field(user_id, field_name='user_id')
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if user.email != current_user.email:
            raise HTTPException(status_code=403, detail="Forbidden to update")

        updated_user = await self.user_crud.update(user, user_data.dict())
        return updated_user

    async def delete_user(self, user_id: int, email: str) -> None:
        current_user = await self.user_crud.get_by_field(email, field_name='email')
        user = await self.user_crud.get_by_field(user_id, field_name='user_id')
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if user.email != current_user.email:
            raise HTTPException(status_code=403, detail="Forbidden to delete")

        deleted_user = await self.user_crud.delete(user)
        return deleted_user
