from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from fastapi_pagination import Page, Params, paginate

from schemas.users import ShowUser, UserCreate, DeleteUserResponse, UpdatedUserResponse, UpdateUserRequest, DeactivateUserRequest
from services.users import UsersService
from utils.dependencies import get_users_service
from utils.security import decode_bearer_token

users_router = APIRouter()


def get_user_data(user_data: dict = Depends(decode_bearer_token)):
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found")
    email = user_data.get("email", None)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not found in token data")
    return email


@users_router.get("/users/", response_model=Page[ShowUser])
async def get_all_users(params: Params = Depends(), user_email: str = Depends(get_user_data),
                        users_service: UsersService = Depends(get_users_service)):
    users = await users_service.get_all_users()
    if users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return paginate(users, params)


@users_router.get("/user/{user_id}", response_model=ShowUser)
async def get_user_by_id(user_id: int = Path(...), user_email: str = Depends(get_user_data),
                         users_service: UsersService = Depends(get_users_service)):
    user = await users_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@users_router.post("/user/", response_model=ShowUser)
async def create_user(user: UserCreate = Body(...), users_service: UsersService = Depends(get_users_service)):
    created_user = await users_service.create_user(user)
    return created_user


@users_router.put("/user/{user_id}", response_model=UpdatedUserResponse)
async def update_user(user_id: int = Path(...), user: UpdateUserRequest = Body(...),
                      user_email: str = Depends(get_user_data),
                      users_service: UsersService = Depends(get_users_service)):
    updated_user = await users_service.update_user(user_id, user, user_email)
    return {"updated_user_id": updated_user.user_id}


@users_router.delete("/user/{user_id}", response_model=DeleteUserResponse)
async def deactivate_user(user_id: int = Path(...), user_email: str = Depends(get_user_data),
                          users_service: UsersService = Depends(get_users_service)):
    deactivated_user = await users_service.deactivate_user(user_id, user_data=DeactivateUserRequest(is_active=False))
    return {"deactivated_user": deactivated_user.user_id}
