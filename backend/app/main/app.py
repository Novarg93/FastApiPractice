from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.routes.items import router as items_router
from app.routes.auth import router as auth_router
app = FastAPI()

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
@app.get("/")
def read_root():
    return {"message": "API is working!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main.app:app", host="127.0.0.1", port=8000, reload=True)
