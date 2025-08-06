from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.orders import Order, OrderItem
from app.models.users import User
from app.schemas.orders import OrderCreate, OrderRead
from app.core.security import get_current_user
from app.models.items import Item

router = APIRouter(prefix="/orders", tags=["orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=[OrderRead])
def create_order(order_data: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not order_data.items:
        raise HTTPException(status_code=404, detail="No items")

    new_order = Order(user_id=current_user.id, status="Pending")
    db.add(new_order)
    db.flush()

    for item_data in order_data.items:
        db_item = db.query(Item).filter(Item.id == item_data.id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")

        order_item = OrderItem(
            order_id=new_order.id,
            item_id=db_item.id,
            quantity=item_data.quantity,
            price=item_data.price,
        )
        db.add(order_item)

    db.commit()
    db.refresh(new_order)
    return new_order

@router.get('/', response_model=list[OrderRead])
def get_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Order).filter(Order.user_id == current_user.id).all()