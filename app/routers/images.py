from typing import List

from app.cruds import posts as crud_post
from app.cruds import images as crud_image
from app.custom_expetion import ImageException
from app.dependencies import get_current_user, get_db, have_user_permission
from app.file_service import max_image_size_KB
from app.models.account_type import AccountType
from app.schemats.posts import PostResponse
from app.schemats.users import User, UserCreate, UserEdit, UserEditMe, UserResponse
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter(tags=["images"])


@router.post("/image/post_id/", response_model=PostResponse, status_code=201)
async def add_image(
        post_id: int,
        image: UploadFile = File(default=None),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    post = crud_post.get_post_by_id(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        have_user_permission(current_user, [AccountType.ADMIN])

    try:
        await crud_image.create_image(db, post_id, image)
    except ImageException:
        raise HTTPException(
            status_code=400,
            detail="You must sent correct image (only MIME image/jpg and image/png) and image size "
                   "can be up to " + str(max_image_size_KB) + " KB",
        )
    return crud_post.get_post_by_id(db, post_id)
