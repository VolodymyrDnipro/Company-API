from fastapi import APIRouter, Depends, HTTPException, status

from schemas.users import ShowUser, ShowAllUsers, UserCreate, DeleteUserResponse, UpdatedUserResponse, UpdateUserRequest
from services.users import UsersService
from utils.dependencies import get_users_service
from utils.security import decode_bearer_token

users_router = APIRouter()


@users_router.get("/users/", response_model=ShowAllUsers)
async def get_all_users(user_data: dict = Depends(decode_bearer_token), users_service: UsersService = Depends(get_users_service)):
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found")
    email = user_data.get("email", None)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not found in token data")

    users = await users_service.get_all_users()
    if users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return {"users": users}


@users_router.get("/user/{user_id}", response_model=ShowUser)
async def get_user_by_id(user_id: int, user_data: dict = Depends(decode_bearer_token), users_service: UsersService = Depends(get_users_service)):
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found")
    email = user_data.get("email", None)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not found in token data")

    user = await users_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@users_router.post("/user/", response_model=ShowUser)
async def create_user(user: UserCreate, user_data: dict = Depends(decode_bearer_token), users_service: UsersService = Depends(get_users_service)):
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found")
    email = user_data.get("email", None)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not found in token data")

    created_user = await users_service.create_user(user)
    return created_user


@users_router.put("/user/{user_id}", response_model=UpdatedUserResponse)
async def update_user(user_id: int, user: UpdateUserRequest, user_data: dict = Depends(decode_bearer_token), users_service: UsersService = Depends(get_users_service)):
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found")
    email = user_data.get("email", None)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not found in token data")

    updated_user = await users_service.check_user_before_update(user_id, user, email)
    return {"updated_user_id": updated_user.user_id}


@users_router.delete("/user/{user_id}", response_model=DeleteUserResponse)
async def delete_user(user_id: int, user_data: dict = Depends(decode_bearer_token), users_service: UsersService = Depends(get_users_service)):
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found")
    email = user_data.get("email", None)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not found in token data")

    await users_service.check_user_before_delete(user_id, email)
    return {"deleted_user_id": user_id}
