from typing import List

from fastapi import Depends, APIRouter, HTTPException, File, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, schema
from app.custom_expetion import ImageException
from app.dependencies import get_db, get_current_user, have_user_permission
from app.file_service import max_image_size_KB
from app.models.account_type import AccountType
from app.schema import UserResponse, User, UserEdit

router = APIRouter(tags=["user"])


@router.get("/users", response_model=List[UserResponse])
async def get_organizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users_by_type(db, AccountType.ORGANIZATION, skip, limit)

    return users


@router.get("/admin/users", response_model=List[UserResponse], responses={
    401: {
        "description": "Not authenticated, you must have Admin permission"
    }
})
async def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    have_user_permission(current_user, [AccountType.ADMIN])
    users = crud.get_users(db, skip, limit)

    return users


@router.get("/users/me", response_model=UserResponse)
async def get_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/users/{user_id}", response_model=UserResponse, responses={
    404: {
        "description": "User not found"
    }
})
async def get_user_by_user_id(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_userid(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: schema.UserCreate = Depends(schema.UserCreate.as_form),
                      avatar: UploadFile = File(default=None),
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    have_user_permission(current_user, [AccountType.ADMIN])
    try:
        user = await crud.create_user(db, user, avatar)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User with this email or username already exists")
    except ImageException:
        raise HTTPException(status_code=400,
                            detail="You must sent correct image (only MIME image/jpg and image/png) and image size "
                                   "can be up to " + str(max_image_size_KB) + " KB")
    return user


@router.patch("/users/me", response_model=UserResponse)
async def edit_user_me(userData: schema.UserEditMe = Depends(schema.UserEditMe.as_form),
                       new_avatar: UploadFile = File(default=None), db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    data = UserEdit(**userData.dict())
    try:
        user = await crud.update_user(db, current_user, data, new_avatar)
    except ImageException:
        raise HTTPException(status_code=400,
                            detail="You must sent correct image (only MIME image/jpg and image/png) and image size "
                                   "can be up to" + max_image_size_KB + " KB")
    return user


@router.patch("/users/{user_id}", response_model=UserResponse)
async def edit_user_by_user_id(user_id: int, userData: schema.UserEdit = Depends(schema.UserEdit.as_form),
                               new_avatar: UploadFile = File(default=None), db: Session = Depends(get_db),
                               current_user: User = Depends(get_current_user)):
    have_user_permission(current_user, [AccountType.ADMIN])
    try:
        user = crud.get_user_by_userid(db, user_id, new_avatar)
    except ImageException:
        raise HTTPException(status_code=400,
                            detail="You must sent correct image (only MIME image/jpg and image/png) and image size "
                                   "can be up to" + max_image_size_KB + " KB")
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_response = crud.update_user(db, user, userData)

    return user_response


@router.delete("/users/{user_id}")
async def delete_user_by_user_id(user_id: int, db: Session = Depends(get_db),
                                 current_user: User = Depends(get_current_user)):
    have_user_permission(current_user, [AccountType.ADMIN])
    user = crud.get_user_by_userid(db, user_id)
    if user == current_user:
        raise HTTPException(status_code=400, detail="You cannot delete yourself")
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user)

    return {"message": "Deleted"}
