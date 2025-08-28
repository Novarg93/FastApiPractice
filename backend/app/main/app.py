import stripe
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path

from app.services import cart
from app.routes import games, categories, search, chat, product_options, products
from app.routes.items import router as items_router
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.orders import router as orders_router
from app.stripe.stripe_success import router as stripe_success_router
from app.core.settings import settings
import app.models  # noqa: F401

stripe.api_key = settings.STRIPE_API_KEY

@asynccontextmanager
async def lifespan(app: FastAPI):
    Path(settings.MEDIA_ROOT).mkdir(parents=True, exist_ok=True)
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

app.include_router(users_router)
app.include_router(games.router)
app.include_router(categories.router)
app.include_router(items_router)
app.include_router(auth_router)
app.include_router(orders_router)
app.include_router(stripe_success_router)
app.include_router(search.router)
app.include_router(cart.router)
app.include_router(chat.router)
app.include_router(products.router)
app.include_router(product_options.router)


app.mount(settings.MEDIA_URL, StaticFiles(directory=settings.MEDIA_ROOT), name="media")

@app.get("/")
def read_root():
    return {"message": "SANYA"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main.app:app", host="127.0.0.1", port=8000, reload=True)
