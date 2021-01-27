from datetime import datetime

from sqlalchemy import Column, Integer, String, Enum, DateTime, NUMERIC
from sqlalchemy.orm import relationship

from .post_type import PostType
from ..database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(PostType), default=PostType.COLLECTION)
    date = Column(DateTime, default=datetime.now())
    title = Column(String(100))
    desc = Column(String(700))
    long = Column(NUMERIC)
    lat = Column(NUMERIC)

    images = relationship("Images")

    author = relationship("User", back_populates="posts")
