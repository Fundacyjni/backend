from fastapi import UploadFile
from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import models, schema
from .custom_expetion import ImageException
from .file_service import save_file
from .models.account_type import AccountType
import hashlib

from .schema import User

allowed_MIME = ["image/jpeg", "image/png"]


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_users_by_type(
        db: Session, account_type: AccountType, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.User)
            .filter(models.User.type == account_type)
            .offset(skip)
            .limit(limit)
            .all()
    )


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_userid(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def login_user(db, username: str, password: str):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return db.query(models.User).filter(
        and_(models.User.password == hashed_password,
             models.User.username == username)).first()


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def get_post_by_id(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def create_post(db: Session, post: schema.PostCreate, user):
    db_item = models.Post(**post.dict(), author_id=user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def edit_post(db: Session, post: models.Post, post_data: schema.PostEdit):
    if post_data.title is not None:
        post.title = post_data.title
    if post_data.type is not None:
        post.type = post_data.type
    if post_data.desc is not None:
        post.desc = post_data.desc
    if post_data.long is not None:
        post.long = post_data.long
    if post_data.lat is not None:
        post.lat = post_data.lat
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post: models.Post):
    db.delete(post)
    db.commit()
    return post


async def create_user(db: Session, user: schema.UserCreate, avatar: UploadFile = None):
    user.password = hashlib.sha256(user.password.encode('utf-8')).hexdigest()
    if user.visible_name is None:
        user.visible_name = user.username
    image_url = ""
    if avatar is not None:
        if avatar.content_type not in allowed_MIME:
            raise ImageException()

        data = await avatar.read()
        extension = avatar.filename.split('.')[-1]
        image_url = save_file(data, extension)

    db_user = models.User(
        username=user.username,
        password=user.password,
        visible_name=user.visible_name,
        desc=user.desc,
        email=user.email,
        image=image_url,
        type=AccountType(user.type)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: User, userData: schema.UserEdit):
    if userData.visible_name is not None:
        user.visible_name = userData.visible_name
    if userData.desc is not None:
        user.desc = userData.desc
    if userData.type is not None:
        user.type = userData.type
    if userData.password is not None:
        password = hashlib.sha256(userData.password.encode('utf-8')).hexdigest()
        user.password = password

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()
