from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app import crud
from app.dependencies import get_db
from app.models.account_type import AccountType
from app.schema import PostResponse

router = APIRouter(tags=["post"])


@router.get("/posts", response_model=List[PostResponse])
async def get_organizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip, limit)
    return posts

@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_organizations(post_id, db: Session = Depends(get_db)):
    posts = crud.get_post_by_id(db, post_id)
    return posts
