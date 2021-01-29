from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app import crud
from app.dependencies import get_db
from app.models.account_type import AccountType
from app.schema import UserResponse

router = APIRouter(tags=["user"])


@router.get("/users", response_model=List[UserResponse])
async def get_organizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users_by_type(db, AccountType.ORGANIZATION, skip, limit)
    return users
