from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from fastapi import Query
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
                                {
                                    "id": 1,
                                    "url": "exampleWeb.pl/url/to/image2"
                                },
                                {
                                    "id": 2,
                                    "url": "exampleWeb.pl/url/to/image3"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        orm_mode = True


class PostResponse(Post):
    author: User = None

    class Config:
        orm_mode = True


class UserResponse(User):
    posts: List[Post] = []

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str = Query(None, min_length=6, max_length=20)
    password: str = Query(None, min_length=7, max_length=50,
                          regex="^.*(?=.{8,})((?=.*[!@#$%^&*()\-_=+{};:,<.>]){1})(?=.*\d)((?=.*[a-z]){1})((?=.*["
                                "A-Z]){1}).*$")
    visible_name: Optional[str] = Query(None, min_length=6, max_length=40)
    desc: Optional[str] = Query(None, max_length=400)
    email: str = Query(None, max_length=50)
    # TOOO(any): Send file
    type: Optional[AccountType] = AccountType.ORGANIZATION


class UserEditMe(BaseModel):
    visible_name: Optional[str] = Query(None, min_length=6, max_length=40)
    desc: Optional[str] = Query(None, max_length=400)
    password: Optional[str] = Query(None, min_length=5, max_length=50,
                                    regex="^.*(?=.{8,})((?=.*[!@#$%^&*()\-_=+{};:,<.>]){1})(?=.*\d)((?=.*[a-z]){1})((?=.*["
                                          "A-Z]){1}).*$")


class UserEdit(UserEditMe):
    type: Optional[AccountType] = None


class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
