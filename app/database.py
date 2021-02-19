import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

server = os.getenv("serverDB")
if server is None:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
else:
    username = os.getenv("usernameDB")
    password = os.getenv("passwordDB")
    SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s" % (username, password, server)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
