import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

from ..database import Base


class PostType(enum.Enum):
    COLLECTION = 1
    MONETARY = 2


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(PostType), default=PostType.COLLECTION)
    date = Column(String, default=datetime.now())
    title = Column(String(100))
    desc = Column(String(700))
    long = Column(DECIMAL, nullable=True)
    lat = Column(DECIMAL, nullable=True)

    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts", cascade="save-update")

    # images = relationship("Images", back_populates="post")
