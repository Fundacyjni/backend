from typing import List

from fastapi import Depends, APIRouter, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import crud, schema
from app.dependencies import get_db, get_current_user, have_user_permission
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
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    have_user_permission(current_user, [AccountType.ADMIN])
    try:
        user = crud.create_user(db, user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User with this email or username already exists")

    return user


@router.patch("/users/me", response_model=UserResponse)
async def edit_user_me(userData: schema.UserEditMe, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    data = UserEdit(**userData.dict())
    user = crud.update_user(db, current_user, data)

    return user


@router.patch("/users/{user_id}", response_model=UserResponse)
async def edit_user_by_user_id(user_id: int, userData: schema.UserEdit, db: Session = Depends(get_db),
                               current_user: User = Depends(get_current_user)):
    have_user_permission(current_user, [AccountType.ADMIN])
    user = crud.get_user_by_userid(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_response = crud.update_user(db, user, userData)

    return user_response


@router.delete("/users/{user_id}")
async def edit_user_by_user_id(user_id: int, db: Session = Depends(get_db),
                               current_user: User = Depends(get_current_user)):
    have_user_permission(current_user, [AccountType.ADMIN])
    user = crud.get_user_by_userid(db, user_id)
    if user == current_user:
        raise HTTPException(status_code=400, detail="You cannot delete yourself")
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user)

    return {"message": "Deleted"}
