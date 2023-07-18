from typing import List
from db.models.users import User
from hashing import Hasher
from managers.user_manager import CRUDBase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from schemas.users import UserCreate, UpdateUserRequest


class UsersService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_crud = CRUDBase[User](User, session)

    async def get_all_users(self) -> List[User]:
        return await self.user_crud.get_all()

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.user_crud.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def create_user(self, user_data: UserCreate) -> User:
        hashed_password = Hasher.get_password_hash(user_data.password)
        user = User(name=user_data.name, surname=user_data.surname, email=user_data.email,
                    hashed_password=hashed_password)
        created_user = await self.user_crud.create(user)
        return created_user

    async def update_user(self, user_id: int, user_data: UpdateUserRequest) -> User:
        existing_user = await self.user_crud.get_by_id(user_id)
        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        updated_user = await self.user_crud.update(existing_user, user_data.dict())
        return updated_user

    async def delete_user(self, user_id: int) -> None:
        existing_user = await self.user_crud.get_by_id(user_id)
        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        await self.user_crud.delete(existing_user)
