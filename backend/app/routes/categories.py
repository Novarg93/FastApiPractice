# app/routes/categories.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models import Category
from app.schemas.categories import CategoryRead

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("", response_model=list[CategoryRead])
def list_categories(game_id: int = Query(...), db: Session = Depends(get_db)):
    return db.query(Category).filter(Category.game_id == game_id).all()
