from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models import Item
from app.schemas.global_search import ItemSearchResponse

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/items", response_model=list[ItemSearchResponse])
def search_items(
    q: str = Query(..., min_length=2),
    limit: int = 10,
    db: Session = Depends(get_db)
):
    items = (
        db.query(Item.id, Item.name, Item.price, Item.image)
        .filter(Item.name.ilike(f"%{q}%"))
        .limit(limit)
        .all()
    )
    return items
