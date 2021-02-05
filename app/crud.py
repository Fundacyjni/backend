from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import models, schema
from .models.account_type import AccountType
import hashlib

from .schema import User


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_users_by_type(db: Session, account_type: AccountType, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.type == account_type).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_userid(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def login_user(db, username: str, password: str):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return db.query(models.User).filter(
        and_(models.User.password == hashed_password,
             models.User.username == username)).first()


def create_user(db: Session, user: schema.UserCreate):
    user.password = hashlib.sha256(user.password.encode('utf-8')).hexdigest()
    if user.visible_name is None:
        user.visible_name = user.username
    db_user = models.User(
        username=user.username,
        password=user.password,
        visible_name=user.visible_name,
        desc=user.desc,
        email=user.email,
        image="Sciezka",
        type=user.type
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
