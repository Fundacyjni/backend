from datetime import datetime

from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship

from .account_type import AccountType
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(AccountType), default=AccountType.USER)
    date = Column(DateTime, default=datetime.now())
    username = Column(String(20), unique=True, index=True)
    visible_name = Column(String(40))
    desc = Column(String(400))
    email = Column(String(50), unique=True, index=True)
    password = Column(String)

    image = Column(String(id))

    posts = relationship("Post", back_populates="author")
