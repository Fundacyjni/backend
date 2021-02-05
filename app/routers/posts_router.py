from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.dependencies import get_db
from app.models.account_type import AccountType
from app.schema import PostResponse, PostCreate

router = APIRouter(tags=["post"])


@router.get("/posts", response_model=List[PostResponse])
async def get_all_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip, limit)
    if posts is None:
        raise HTTPException(status_code=404, detail="Posts not found")
    return posts


@router.post("/posts", response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    posts = crud.create_post(db, post)
    return posts


@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id, db: Session = Depends(get_db)):
    posts = crud.get_post_by_id(db, post_id)
    if posts is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return posts


@router.patch("/posts/{post_id}", response_model=PostResponse)
async def edite_post(post_id, db: Session = Depends(get_db)):
    pass
    # TODO: Do patch


@router.delete("/posts/{post_id}", response_model=PostResponse)
async def delete_post(post_id, db: Session = Depends(get_db)):
    posts = crud.get_post_by_id(db, post_id)
    if posts is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.delete_post(db, posts)
