from logging import getLogger
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from managers.user_manager import _get_user_by_id
from managers.user_manager import _get_users_all
from managers.user_manager import _create_new_user
from managers.user_manager import _delete_user
from managers.user_manager import _update_user

from schemas.users import DeleteUserResponse, ShowUser, ShowAllUsers, UpdatedUserResponse, UpdateUserRequest, UserCreate
from db.session import get_db

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db), ) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return user


@user_router.get("/all", response_model=ShowAllUsers)
async def get_all_users(db: AsyncSession = Depends(get_db)) -> List[ShowUser]:
    users = await _get_users_all(db)
    if users is None:
        raise HTTPException(status_code=404, detail=f"Users not found.")
    return users


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db), ) -> DeleteUserResponse:
    user_for_deletion = await _get_user_by_id(user_id, db)
    if user_for_deletion is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(user_id: UUID, body: UpdateUserRequest, db: AsyncSession = Depends(get_db)) -> UpdatedUserResponse:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(status_code=422, detail="At least one parameter for user update info should be provided",)
    user_for_update = await _get_user_by_id(user_id, db)
    if user_for_update is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    try:
        updated_user_id = await _update_user(updated_user_params=updated_user_params, session=db, user_id=user_id)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)
