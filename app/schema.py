from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel

from app.models.account_type import AccountType
from app.models.post_type import PostType


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
    images: List[Images]

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    type: AccountType
    date: datetime = None
    username: str
    visible_name: str
    desc: str
    email: str
    desc: str

    image: str

    class Config:
        orm_mode = True


class PostResponse(Post):
    author: User = None

    class Config:
        orm_mode = True


class UserResponse(User):
    posts: List[Post] = []

    class Config:
        orm_mode = True
