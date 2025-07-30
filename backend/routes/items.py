from fastapi import APIRouter, Depends, Query, HTTPException, Path
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.items import Item
from database.session import get_db
from schemas.items import ItemCreate
from database.currency_script import seed_items

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", name="list items")
async def read_items(
    limit: int = Query(5, ge=1),
    offset: int = Query(0, ge=0),
    sort_by: str = Query("name", pattern="^(name|price)$"),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Item)
    stmt = stmt.order_by(Item.name) if sort_by == "name" else stmt.order_by(Item.price)
    total = (await db.execute(select(func.count()).select_from(Item))).scalar_one()
    result = await db.execute(stmt.limit(limit).offset(offset))
    items = result.scalars().all()
    return {"items": items, "count": total}

@router.get("/{item_id}", name="get item by id")
async def read_item(
    item_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/", response_model=ItemCreate, status_code=201, name="create item")
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db)
):
    new_item = Item(**item.model_dump())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.post("/seed", tags=["seed"])
async def seed_items_route(db: AsyncSession = Depends(get_db)):
    await seed_items(db)
    return {"status": "ok"}
