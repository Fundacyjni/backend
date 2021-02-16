from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from .. import crud
from ..dependencies import get_db
from ..models import AccountType, User
from ..schema import PostResponse, PostCreate, PostEdit
from ..dependencies import get_current_user

router = APIRouter(tags=["post"])


@router.get(
    "/posts",
    response_model=List[PostResponse],
    responses={404: {"description": "Post not found"}},
)
async def get_all_posts(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    order: Optional[str] = "-date",
    long: Optional[float] = None,
    lat: Optional[float] = None,
    db: Session = Depends(get_db),
):
    posts = crud.get_posts(db, skip, limit, search, order, lat, long)
    if posts is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return posts


@router.post(
    "/posts",
    response_model=PostResponse,
    responses={404: {"description": "Post not found"}},
)
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    posts = crud.create_post(db, post, current_user)
    return posts


@router.get(
    "/posts/{post_id}",
    response_model=PostResponse,
    responses={404: {"description": "Post not found"}},
)
async def get_post(post_id, db: Session = Depends(get_db)):
    posts = crud.get_post_by_id(db, post_id)
    if posts is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return posts


@router.patch(
    "/posts/{post_id}",
    response_model=PostResponse,
    responses={
        404: {"description": "Post not found"},
        401: {"description": "Not authenticated, you must have Admin permission"},
    },
)
async def edit_post(
    post_id,
    post_data: PostEdit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = crud.get_post_by_id(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        have_user_permission(current_user, [AccountType.ADMIN])

    post = crud.edit_post(db, post, post_data)
    return post


@router.delete(
    "/posts/{post_id}",
    response_model=PostResponse,
    responses={404: {"description": "Post not found"}},
)
async def delete_post(
    post_id,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    posts = crud.get_post_by_id(db, post_id)
    if posts is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.delete_post(db, posts)
