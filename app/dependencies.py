import hashlib
import os
import secrets
import random
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .cruds import users
from .database import SessionLocal
from .models import User
from .models.account_type import AccountType
from .schemats.users import TokenData

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

SECRET_KEY = os.environ.get("secretKey")
if SECRET_KEY is None:
    SECRET_KEY = secrets.token_hex(32)

SECRET_SALT = os.environ.get("secretSalt")
if SECRET_SALT is None:
    SECRET_SALT = ""
    for i in range(16):
        SECRET_SALT += random.choice(ALPHABET)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
        token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = users.get_user_by_email(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


def have_user_permission(current_user: User, permission: List[AccountType]):
    if current_user.type not in permission:
        raise HTTPException(
            status_code=401, detail="You don't have permission to do this"
        )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def encrypt_sha256_with_salt(password):
    salted_pass = password + SECRET_SALT
    return hashlib.sha256(salted_pass.encode("utf-8")).hexdigest()
