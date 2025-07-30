from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.items import Item
from database.session import get_db

router = APIRouter()

@router.get("/", name="list items")
async def read_items(
    limit: int = Query(5, ge=1),
    offset: int = Query(0, ge=0),
    sort_by: str = Query("name", regex="^(name|price)$"),
    db: AsyncSession = Depends(get_db)
): 
    stmt = select(Item)
    stmt = stmt.order_by(Item.name) if sort_by == "name" else stmt.order_by(Item.price)
    total = (await db.execute(select(func.count())))