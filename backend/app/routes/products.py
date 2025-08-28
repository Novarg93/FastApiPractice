from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.items import Item
from app.schemas.items import ItemCreate, ItemRead, ItemUpdate, ItemListResponse
from app.models.users import User, UserRole
from app.core.security import get_current_user

router = APIRouter(prefix="/products", tags=["products"])

# Создать продукт
@router.post("/", response_model=ItemRead)
def create_product(
    data: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPPORT]:
        raise HTTPException(status_code=403, detail="Not authorized")

    product = Item(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


# Список продуктов
@router.get("/", response_model=ItemListResponse)
def list_products(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return {"items": items, "total": len(items)}


# Получить продукт
@router.get("/{product_id}", response_model=ItemRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Item).filter(Item.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Обновить продукт
@router.patch("/{product_id}", response_model=ItemRead)
def update_product(
    product_id: int,
    data: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPPORT]:
        raise HTTPException(status_code=403, detail="Not authorized")

    product = db.query(Item).filter(Item.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


# Удалить продукт
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPPORT]:
        raise HTTPException(status_code=403, detail="Not authorized")

    product = db.query(Item).filter(Item.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"ok": True}
