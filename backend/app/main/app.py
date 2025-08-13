# backend/app/main/app.py
from venv import create

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.routes.items import router as items_router
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.database.session import engine, Base
import app.models  # noqa: F401

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items_router)
app.include_router(auth_router)
app.include_router(users_router)

from app.core.settings import settings
app.mount(settings.MEDIA_URL, StaticFiles(directory=settings.MEDIA_ROOT), name="media")

@app.get("/")
def read_root():
    return {"message": "SANYA"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main.app:app", host="127.0.0.1", port=8000, reload=True)
