from datetime import datetime
from decimal import Decimal
from typing import Optional

from app.models.post import PostType
from pydantic import BaseModel

# from .users import User


class Images(BaseModel):
    id: int
    url: str

    class Config:
        orm_mode = True


class Post(BaseModel):
    id: int
    type: PostType
    date: datetime = None
    title: str
    desc: str
    long: Decimal
    lat: Decimal
    url: Optional[str]
    # images: List[Images]

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    title: str
    type: PostType
    desc: str
    long: Decimal
    lat: Decimal
    url: Optional[str]
    # images: List[Images]

    class Config:
        orm_mode = True


class PostEdit(BaseModel):
    title: Optional[str]
    desc: Optional[str]
    long: Optional[Decimal]
    lat: Optional[Decimal]
    url: Optional[str]
    # images: List[Images]

    class Config:
        orm_mode = True


class PostResponse(Post):
    # TODO: fix
    # author: User = None

    class Config:
        orm_mode = True
