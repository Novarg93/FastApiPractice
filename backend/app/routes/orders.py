from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database.session import get_db
from app.models.orders import Order, OrderItem
from app.models.users import User
from app.schemas.orders import OrderCreate, OrderRead
from app.core.security import get_current_user
from app.services.orders import create_order_service, checkout_service
from app.services.chat_service import create_chat_for_order

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderRead)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    order = create_order_service(db, current_user.id, order_data)
    create_chat_for_order(db, order.id, client_id=current_user.id)

    return order


@router.post("/checkout")
def checkout(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order_id = payload.get("order_id")
    payment_method = payload.get("payment_method")

    if not order_id or not payment_method:
        raise HTTPException(status_code=400, detail="order_id and payment_method required")

    return checkout_service(db, order_id, current_user.id, payment_method)


@router.get("/me", response_model=List[OrderRead])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.item),
        joinedload(Order.user)
    ).filter(Order.user_id == current_user.id).all()


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.item),
        joinedload(Order.user)
    ).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get('/', response_model=list[OrderRead])
def get_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Order).filter(Order.user_id == current_user.id).all()
