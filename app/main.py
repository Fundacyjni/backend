from fastapi import FastAPI
from .database import engine, Base
from .routers import users_router, auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fundacyjni API",
    description="",
    version="0.0.2"
)
app.include_router(users_router.router)
app.include_router(auth_router.router)
