from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.items import Item
from schemas.items import ItemCreate, ItemUpdate, ItemResponse
from database.session import get_db

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[ItemResponse])
async def read_items(
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1),
    q: str = Query("", alias="q"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Item)
    if q:
        stmt = stmt.filter(Item.title.ilike(f"%{q}%"))
    stmt = stmt.offset((page - 1) * limit).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/count", response_model=dict)
async def get_items_count(
    q: str = Query("", alias="q"),
    db: AsyncSession = Depends(get_db),
):
    from sqlalchemy import func
    if q:
        subq = select(Item).filter(Item.title.ilike(f"%{q}%")).subquery()
        stmt = select(func.count()).select_from(subq)
    else:
        stmt = select(func.count()).select_from(Item)
    result = await db.execute(stmt)
    return {"count": result.scalar_one()}


@router.get("/{item_id}", response_model=ItemResponse)
async def read_item(
    item_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Item).filter_by(id=item_id))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Товар с ID {item_id} не найден")
    return item


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_data: ItemCreate,
    db: AsyncSession = Depends(get_db),
):
    new_item = Item(
        title=item_data.title,
        price=int(item_data.price * 100),
        description=item_data.description,
        image_url=item_data.image_url,
    )
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_data: ItemUpdate,
    item_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_db), 
):
    result = await db.execute(select(Item).filter_by(id=item_id))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Товар с ID {item_id} не найден")
    item.title = item_data.title
    item.price = int(item_data.price * 100)
    item.description = item_data.description
    item.image_url = item_data.image_url
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/{item_id}", response_model=dict)
async def delete_item(
    item_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Item).filter_by(id=item_id))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Товар с ID {item_id} не найден")
    await db.delete(item)
    await db.commit()
    return {"message": "Товар успешно удалён"}
