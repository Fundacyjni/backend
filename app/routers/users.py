from typing import List

from app.cruds import users
from app.custom_expetion import ImageException
from app.dependencies import get_current_user, get_db, have_user_permission
from app.file_service import max_image_size_KB
from app.models.account_type import AccountType
from app.schemats import users
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter(tags=["user"])


@router.get("/users", response_model=List[users.UserResponse])
async def get_organizations(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    users = users.get_users_by_type(db, AccountType.ORGANIZATION, skip, limit)

    return users


@router.get(
    "/admin/users",
    response_model=List[users.UserResponse],
    responses={
        401: {"description": "Not authenticated, you must have Admin permission"}
    },
)
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user),
):
    have_user_permission(current_user, [AccountType.ADMIN])
    users = users.get_users(db, skip, limit)

    return users


@router.get("/users/me", response_model=users.UserResponse)
async def get_user_me(current_user: users.User = Depends(get_current_user)):
    return current_user


@router.get(
    "/users/{user_id}",
    response_model=users.UserResponse,
    responses={404: {"description": "User not found"}},
)
async def get_user_by_user_id(user_id: int, db: Session = Depends(get_db)):
    user = users.get_user_by_userid(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/users", response_model=users.UserResponse, status_code=201)
async def create_user(
    user: users.UserCreate = Depends(users.UserCreate.as_form),
    avatar: UploadFile = File(default=None),
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user),
):
    have_user_permission(current_user, [AccountType.ADMIN])

    try:
        user = await users.create_user(db, user, avatar)
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="User with this email or username already exists"
        )
    except ImageException:
        raise HTTPException(
            status_code=400,
            detail="You must sent correct image (only MIME image/jpg and image/png) and image size "
            "can be up to " + str(max_image_size_KB) + " KB",
        )
    return user


@router.patch("/users/me", response_model=users.UserResponse)
async def edit_user_me(
    userData: users.UserEditMe = Depends(users.UserEditMe.as_form),
    new_avatar: UploadFile = File(default=None),
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user),
):
    data = UserEdit(**userData.dict())
    try:
        user = await users.update_user(db, current_user, data, new_avatar)
    except ImageException:
        raise HTTPException(
            status_code=400,
            detail="You must sent correct image (only MIME image/jpg and image/png) and image size "
            "can be up to" + max_image_size_KB + " KB",
        )
    return user


@router.patch("/users/{user_id}", response_model=users.UserResponse)
async def edit_user_by_user_id(
    user_id: int,
    userData: users.UserEdit = Depends(users.UserEdit.as_form),
    new_avatar: UploadFile = File(default=None),
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user),
):
    have_user_permission(current_user, [AccountType.ADMIN])
    try:
        user = users.get_user_by_userid(db, user_id, new_avatar)
    except ImageException:
        raise HTTPException(
            status_code=400,
            detail="You must sent correct image (only MIME image/jpg and image/png) and image size "
            "can be up to" + max_image_size_KB + " KB",
        )
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_response = users.update_user(db, user, userData)

    return user_response


@router.delete("/users/{user_id}")
async def delete_user_by_user_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user),
):
    have_user_permission(current_user, [AccountType.ADMIN])
    user = users.get_user_by_userid(db, user_id)
    if user == current_user:
        raise HTTPException(status_code=400, detail="You cannot delete yourself")
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    users.delete_user(db, user)

    return {"message": "Deleted"}
