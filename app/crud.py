from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from . import models, schema
from .models.account_type import AccountType
import hashlib

from .schema import User


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


def generateDistance(Post, lat, long):
    x = Post.long - long
    y = Post.lat - lat
    return x * x + y * y


def get_posts(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    order: str = None,
    lat: float = None,
    long: float = None,
    type: models.PostType = None,
):

    bufor = db.query(models.Post)

    if not (type is None):
        bufor = bufor.filter(models.Post.type == type)

    if not (search is None):
        bufor = bufor.filter(
            or_(
                models.Post.title.like("%" + search + "%"),
                models.Post.desc.like("%" + search + "%"),
            )
        )

    if not (lat is None or long is None):
        bufor = bufor.order_by(generateDistance(models.Post, lat, long))
    elif not (order is None):
        if order[0] == "-":
            order = order.split("-", 1)[1]
            bufor = bufor.order_by(getattr(models.Post, order).desc())
        else:
            bufor = bufor.order_by(getattr(models.Post, order))

    return bufor.offset(skip).limit(limit).all()


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


def create_user(db: Session, user: schema.UserCreate):
    user.password = hashlib.sha256(user.password.encode("utf-8")).hexdigest()
    if user.visible_name is None:
        user.visible_name = user.username
    db_user = models.User(
        username=user.username,
        password=user.password,
        visible_name=user.visible_name,
        desc=user.desc,
        email=user.email,
        image="Sciezka",  # TODO(any): Implament sending images
        type=user.type,
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
        password = hashlib.sha256(userData.password.encode("utf-8")).hexdigest()
        user.password = password

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()
