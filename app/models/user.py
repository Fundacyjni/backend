from datetime import datetime

from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base
from .account_type import AccountType


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(AccountType), default=AccountType.ADMIN)
    date = Column(String, default=datetime.now())
    username = Column(String(20), unique=True, index=True)
    visible_name = Column(String(40))
    desc = Column(String(2000))
    email = Column(String(50), unique=True, index=True)
    password = Column(String)
    url = Column(String(500), nullable=True)

    image = Column(String)

    posts = relationship("Post", back_populates="author", cascade="all, delete")
