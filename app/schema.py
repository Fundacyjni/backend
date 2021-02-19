from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel

from app.models.account_type import AccountType
from app.models.post import PostType

regex_security_password = "^.*(?=.{8,})((?=.*[!@#$%^&*()\-_=+{};:,<.>]){1})(?=.*\d)((?=.*[a-z]){1})((?=.*[A-Z]){1}).*$"  # check if password have uppercase and lowercase letters, digitas and special characters
regex_email = "^(.+)@(.+)$"


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


class User(BaseModel):
    id: int
    type: AccountType
    date: datetime = None
    username: str
    visible_name: str
    desc: str
    email: str
    image: str
    url: Optional[str]

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


class UserResponse(User):
    posts: List[Post] = []

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str = Query(None, min_length=2, max_length=100)
    password: str = Query(
        None, min_length=8, max_lengh=100, regex=regex_security_password
    )
    visible_name: Optional[str] = Query(None, min_length=2, max_length=100)
    desc: Optional[str] = Query(None, max_length=400)
    email: str = Query(None, max_length=100, regex=regex_email)
    url: Optional[str]
    # TOOO(any): Send file
    type: Optional[AccountType] = AccountType.ORGANIZATION


class UserEditMe(BaseModel):
    visible_name: Optional[str] = Query(None, min_length=2, max_length=100)
    desc: Optional[str] = Query(None, max_length=400)
    password: Optional[str] = Query(
        None, min_length=8, max_length=100, regex=regex_security_password
    )
    url: Optional[str]


class UserEdit(UserEditMe):
    type: Optional[AccountType]


class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
