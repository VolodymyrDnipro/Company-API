from pydantic import BaseModel, EmailStr
from typing import List


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: str
    email: EmailStr


class UserList(BaseModel):
    users: List[UserBase]


class UserDetail(BaseModel):
    id: int
    username: str
    email: EmailStr
