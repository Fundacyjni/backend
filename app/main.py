from fastapi import FastAPI
from .database import engine, Base
from .routers import users_router, auth_router, posts_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fundacyjni API",
    description="",
    version="0.0.1"
)
app.include_router(users_router.router)
app.include_router(auth_router.router)
app.include_router(posts_router.router)

@app.get("/")
async def root():
    return {"message": "Fundacyjni API, Welcomes you!"}
