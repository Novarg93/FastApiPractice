from fastapi import APIRouter
from schemas.user import UserCreate

router = APIRouter()

 # регистрация пользователя
@router.post("/register")
async def register_user(user: UserCreate):
    return {"message": "ok"}
