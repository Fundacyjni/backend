from sqlalchemy.orm import Session

from . import models
from .models.account_type import AccountType


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_users_by_type(db: Session, account_type: AccountType, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.type == account_type).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_userid(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
