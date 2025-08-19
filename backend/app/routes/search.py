from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models import Item
from app.schemas.global_search import ItemSearchResponse, SearchResponse

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/items", response_model=SearchResponse)
def search_items(
    q: str = Query(..., min_length=2),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    query = db.query(Item).filter(Item.name.ilike(f"%{q}%"))

    total = query.count()
    items = query.limit(limit).all()

    return {"items": items, "total": total}