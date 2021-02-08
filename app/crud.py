from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import models
from . import schema
from .models.account_type import AccountType
import hashlib


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
    hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
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
