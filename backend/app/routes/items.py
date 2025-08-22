from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc, desc

from app.database.session import SessionLocal
from app.models import Category, Game, Item, Option
from app.schemas.items import ItemCreate, ItemRead, ItemListResponse

router = APIRouter(prefix="/items", tags=["items"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=ItemListResponse)
def read_items(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(120, ge=1, le=1000),
    sort_by: str = Query("name", pattern="^(name|price)$"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    q: str = Query("", alias="q"),
):
    query = db.query(Item)
    if q:
        query = query.filter(Item.name.ilike(f"%{q}%"))

    total = query.count()
    sort_column = getattr(Item, sort_by)
    query = query.order_by(asc(sort_column) if order == "asc" else desc(sort_column))
    items = query.offset((page - 1) * limit).limit(limit).all()

    return {"items": items, "total": total}


@router.get("/{item_id}", response_model=ItemRead)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter_by(id=item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item



@router.get("/{game_id}/all", response_model=list[ItemRead])
def items_all(game_id: int, db: Session = Depends(get_db)):
    return db.query(Item).filter(Item.game_id == game_id).all()


@router.get("/{game_id}/{category_slug}", response_model=list[ItemRead])
def items_by_category(game_id: int, category_slug: str, db: Session = Depends(get_db)):
    category = (
        db.query(Category)
        .filter(Category.slug == category_slug, Category.game_id == game_id)
        .first()
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category.items
