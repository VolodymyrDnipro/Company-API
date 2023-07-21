from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession
from managers.user_manager import CRUDBase
from db.models.users import User
from utils.hashing import Hasher


class AuthService:
    async def authenticate_user(self, email: str, password: str, session: AsyncSession) -> Union[User, None]:
        user_crud = CRUDBase[User](User, session)
        user = await user_crud.get_by_field(email, "email")
        if user is None:
            return
        if not Hasher.verify_password(password, user.hashed_password):
            return
        return user

    async def get_user_by_email_for_auth(self, email: str, session: AsyncSession) -> User:
        user_crud = CRUDBase[User](User, session)
        user = await user_crud.get_by_field(email, "email")
        return user
