from fastapi import FastAPI
from .database import engine, Base
from .routers import users_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users_router.router)


@app.get("/")
async def root():
    return {"message": "Hello!"}
