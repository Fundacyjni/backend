from typing import List

from fastapi import UploadFile
from sqlalchemy import or_
from sqlalchemy.orm import Session

from .images import create_image
from .. import models
from ..schemats import posts


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


async def create_post(db: Session, post: posts.PostCreate, user, images: List[UploadFile]):
    db_item = models.Post(**post.dict(), author_id=user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    for image in images:
        await create_image(db, db_item.id, image)

    return db_item


def edit_post(db: Session, post: models.Post, post_data: posts.PostEdit):
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
