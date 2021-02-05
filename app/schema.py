from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel

from app.models.account_type import AccountType
from app.models.post import PostType


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
        schema_extra = {
            "example": [
                {
                    "id": 1,
                    "type": 2,
                    "date": "2020-04-27T00:00:00",
                    "username": "fundation",
                    "visible_name": "fundation example",
                    "desc": "its example description",
                    "email": "fundation@fundation.com",
                    "image": "exampleWeb.pl/url/to/image",
                    "posts": [
                        {
                            "id": 1,
                            "type": 1,
                            "date": "2021-01-29T12:00:00",
                            "title": "example post 1",
                            "desc": "it's example description",
                            "long": 100.01,
                            "lat": 100.4,
                            "images": [
                                {"id": 1, "url": "exampleWeb.pl/url/to/image2"},
                                {"id": 2, "url": "exampleWeb.pl/url/to/image3"},
                            ],
                        }
                    ],
                }
            ]
        }
        orm_mode = True


class PostResponse(Post):
    author: User = None

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    title: str
    type: Decimal
    desc: str
    long: Decimal
    lat: Decimal
    # images: List[Images]

    class Config:
        orm_mode = True


class UserResponse(User):
    posts: List[Post] = []

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
