import re
from typing import Optional, List

from fastapi import HTTPException
from pydantic import BaseModel, field_validator, constr, EmailStr, validator, Field

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")
PASSWORD_PATTERN = re.compile(r"^.+$")


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        from_attributes = True


class ShowUser(TunedModel):
    user_id: int
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class ShowAllUsers(BaseModel):
    users: List[ShowUser]


class UserCreate(BaseModel):
    name: str = Field(..., description="Name of the user")
    surname: str = Field(..., description="Surname of the user")
    email: EmailStr = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the user")

    @field_validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @field_validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class DeleteUserResponse(BaseModel):
    deleted_user_id: int


class UpdatedUserResponse(BaseModel):
    updated_user_id: int


class UpdateUserRequest(BaseModel):
    name: Optional[constr(min_length=1)] = Field(None, description="Updated name of the user")
    surname: Optional[constr(min_length=1)] = Field(None, description="Updated surname of the user")
    password: Optional[constr(min_length=1)] = Field(..., description="Password of the user")

    @field_validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @field_validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value

    @field_validator('password')
    def validate_password(cls, value):
        if not PASSWORD_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Password should not be empty")
        return value
