from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Images(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(100))

    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", back_populates="images")
