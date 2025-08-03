from http.client import responses

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

from app.routes.items import router as items_router
app.include_router(items_router)


@app.get("/")
def read_root():
    return {"message": "API is working!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main.app:app", host="127.0.0.1", port=8000, reload=True)
