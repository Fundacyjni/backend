from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from ..cruds import posts as crud
from ..custom_expetion import ImageException
from ..dependencies import get_current_user, get_db, have_user_permission
from ..file_service import max_image_size_KB
from ..models import AccountType, PostType, User
from ..schemats.posts import PostCreate, PostEdit, PostResponse

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
        type: Optional[int] = None,
        db: Session = Depends(get_db),
):
    if not (type is None):
        type = PostType(type)
    posts = crud.get_posts(db, skip, limit, search, order, lat, long, type)
    if posts is None or posts == []:
        raise HTTPException(status_code=404, detail="Post not found")
    return posts


@router.post(
    "/posts",
    response_model=PostResponse,
    responses={404: {"description": "Post not found"}},
)
async def create_post(
        post: PostCreate = Depends(PostCreate.as_form),
        images: List[UploadFile] = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    try:
        posts = await crud.create_post(db, post, current_user, images)
    except ImageException:
        raise HTTPException(
            status_code=400,
            detail="You must sent correct image (only MIME image/jpg and image/png) and image size "
                   "can be up to " + str(max_image_size_KB) + " KB",
        )
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
    posts = await crud.get_post_by_id(db, post_id)
    if posts is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.delete_post(db, posts)
