from sqlalchemy import Column, Integer, String

from ..database import Base


class Images(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(100))
