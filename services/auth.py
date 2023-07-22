from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from managers.user_manager import CRUDBase
from db.models.users import User
from utils.hashing import Hasher


class AuthService:
    def __init__(self, session: AsyncSession):
        self.user_crud = CRUDBase[User](User, session)

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.user_crud.get_by_field(email, "email")
        if user is None:
            return
        if not Hasher.verify_password(password, user.hashed_password):
            return
        return user

    async def get_user_by_email_for_auth(self, email: str) -> User:
        user = await self.user_crud.get_by_field(email, "email")
        return user
