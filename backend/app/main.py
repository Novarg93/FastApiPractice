from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.init_db import init_db
from routes.items import router as items_router





import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Привет от FastAPI!"}

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(items_router)
