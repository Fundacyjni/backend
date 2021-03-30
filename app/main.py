from fastapi import FastAPI
from starlette.responses import RedirectResponse

from .database import Base, engine
from .routers import auth, posts, users, images

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fundacyjni API", description="", version="0.0.2")
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(images.router)


@app.get("/")
async def root():
    response = RedirectResponse(url="/docs")
    return response
