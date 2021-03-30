from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from fastapi import Form

from app.models.post import PostType
from pydantic import BaseModel


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
    images: List[Images]

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    title: str
    type: PostType
    desc: str
    long: Decimal
    lat: Decimal
    url: Optional[str]

    class Config:
        orm_mode = True

    @classmethod
    def as_form(
            cls,
            title: str = Form(..., min_length=2, max_length=100),
            desc: str = Form(..., max_length=2000),
            long: Decimal = Form(..., lt=180, gt=-180),
            lat: Decimal = Form(..., lt=90, gt=-90),
            url: str = Form("", max_length=500),
            type: int = Form(..., lt=len(PostType) + 1, gt=0),
    ):
        return cls(
            title=title,
            type=type,
            desc=desc,
            long=long,
            lat=lat,
            url=url
        )


class PostEdit(BaseModel):
    title: Optional[str]
    desc: Optional[str]
    long: Optional[Decimal]
    lat: Optional[Decimal]
    url: Optional[str]

    class Config:
        orm_mode = True


from .users import User


class PostResponse(Post):
    author: User = None

    class Config:
        orm_mode = True
