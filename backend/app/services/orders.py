from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.models.orders import Order, OrderItem
from app.models.items import Item
import stripe


def create_order_service(db: Session, user_id: int, order_data):
    if not order_data.items:
        raise HTTPException(status_code=400, detail="No items provided")

    order = Order(user_id=user_id, status="pending", total_price=0)
    db.add(order)
    db.flush()

    total_price = 0
    for item_data in order_data.items:
        db_item = db.query(Item).filter(Item.id == item_data.item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail=f"Item {item_data.item_id} not found")

        db.add(OrderItem(
            order_id=order.id,
            item_id=item_data.item_id,
            quantity=item_data.quantity,
            price=item_data.price
        ))
        total_price += item_data.price * item_data.quantity

    order.total_price = total_price
    db.commit()

    # вернем заказ с подгруженными связями
    order = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.item),
        joinedload(Order.user)
    ).filter(Order.id == order.id).first()

    return order


def checkout_service(db: Session, order_id: int, user_id: int, payment_method: str):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if payment_method == "stripe":
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                mode="payment",
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": f"Order #{order.id}"},
                        "unit_amount": int(order.total_price * 100),
                    },
                    "quantity": 1,
                }],
                success_url="http://localhost:5173/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://localhost:5173/cancel",
                metadata={"order_id": order.id}
            )
            return {"checkout_url": session.url}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    raise HTTPException(status_code=400, detail="Unsupported payment method")