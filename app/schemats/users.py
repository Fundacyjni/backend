from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from app.models.account_type import AccountType
from app.models.post import PostType
from fastapi import Form, Query
from pydantic import BaseModel

from .posts import Post

regex_security_password = "^.*(?=.{8,})((?=.*[!@#$%^&*()\-_=+{};:,<.>]){1})(?=.*\d)((?=.*[a-z]){1})((?=.*[A-Z]){1}).*$"  # check if password have uppercase and lowercase letters, digitas and special characters
regex_email = "^(.+)@(.+)$"


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
    desc: Optional[str] = Query("", max_length=400)
    email: str = Query(None, max_length=100, regex=regex_email)
    url: Optional[str]
    type: Optional[AccountType] = AccountType.ORGANIZATION

    class Config:
        use_enum_values = True
        orm_mode = True

    @classmethod
    def as_form(
        cls,
        username: str = Form(..., min_length=2, max_length=100),
        password: str = Form(
            ..., min_length=8, max_length=100, regex=regex_security_password
        ),
        visible_name: Optional[str] = Form(None, min_length=2, max_length=100),
        desc: Optional[str] = Form("", max_length=400),
        email: str = Form(..., max_length=100, regex=regex_email),
        type: int = Form(AccountType.ORGANIZATION, lt=len(AccountType) + 1, gt=0),
    ):
        return cls(
            username=username,
            password=password,
            visible_name=visible_name,
            desc=desc,
            email=email,
            type=AccountType(type),
        )


class UserEditMe(BaseModel):
    visible_name: Optional[str] = Query(None, min_length=2, max_length=100)
    desc: Optional[str] = Query(None, max_length=400)
    password: Optional[str] = Query(
        None, min_length=8, max_length=100, regex=regex_security_password
    )
    url: Optional[str]

    @classmethod
    def as_form(
        cls,
        password: str = Form(
            None, min_length=8, max_length=100, regex=regex_security_password
        ),
        visible_name: Optional[str] = Form(None, min_length=2, max_length=100),
        desc: Optional[str] = Form(None, max_length=400),
    ):
        return cls(password=password, visible_name=visible_name, desc=desc)


class UserEdit(UserEditMe):
    type: Optional[AccountType]


class TokenData(BaseModel):
    username: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        password: str = Form(
            None, min_length=8, max_length=100, regex=regex_security_password
        ),
        visible_name: Optional[str] = Form(None, min_length=2, max_length=100),
        desc: Optional[str] = Form(None, max_length=400),
        type: Optional[int] = Form(
            AccountType.ORGANIZATION, lt=len(AccountType) + 1, gt=0
        ),
    ):
        return cls(
            password=password,
            visible_name=visible_name,
            desc=desc,
            type=AccountType(type),
        )


class Token(BaseModel):
    access_token: str
    token_type: str
