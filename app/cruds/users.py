import hashlib

from fastapi import UploadFile
from sqlalchemy import and_
from sqlalchemy.orm import Session

from .. import models
from ..dependencies import encrypt_sha256_with_salt
from ..file_service import reupload_image, upload_image
from ..models.account_type import AccountType
from ..schemats import users


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
    hashed_password = encrypt_sha256_with_salt(password)
    return (
        db.query(models.User)
            .filter(
            and_(
                models.User.password == hashed_password,
                models.User.username == username,
            )
        )
            .first()
    )


async def create_user(db: Session, user: users.UserCreate, avatar: UploadFile = None):
    user.password = encrypt_sha256_with_salt(user.password)
    if user.visible_name is None:
        user.visible_name = user.username
    image_url = ""
    if avatar is not None:
        image_url = await upload_image(avatar)
    db_user = models.User(
        username=user.username,
        password=user.password,
        visible_name=user.visible_name,
        desc=user.desc,
        email=user.email,
        image=image_url,
        type=AccountType(user.type),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def update_user(
        db: Session, user: users.User, userData: users.UserEdit, avatar: UploadFile = None
):
    if userData.visible_name is not None:
        user.visible_name = userData.visible_name
    if userData.desc is not None:
        user.desc = userData.desc
    if userData.type is not None:
        user.type = userData.type
    if userData.password is not None:
        password = encrypt_sha256_with_salt(userData.password)
        user.password = password
    if avatar is not None:
        image_url = await reupload_image(user.image, avatar)
        user.image = image_url
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()
