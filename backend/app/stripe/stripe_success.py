from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import stripe

from app.database.session import get_db
from app.models.orders import Order
from app.models.users import User
from app.schemas.orders import OrderRead
from app.core.security import get_current_user

# ← сразу даём префикс /orders, чтобы URL был /orders/stripe/success
router = APIRouter(prefix="/orders", tags=["orders"])

class StripeSuccessResp(BaseModel):
    order: OrderRead
    payment_status: str
    amount_total: float
    currency: str
    session_id: str

@router.get("/stripe/success", response_model=StripeSuccessResp)  # ← GET, не POST
def stripe_success(
    session_id: str = Query(..., description="Stripe Checkout session id"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1) Получаем сессию у Stripe
    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Stripe error: {e}")

    # 2) Достаём order_id из metadata
    meta = getattr(session, "metadata", {}) or {}
    order_id = meta.get("order_id")
    if not order_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="order_id missing in session metadata")

    # 3) Берём ИМЕННО этот заказ текущего пользователя
    order = db.query(Order).filter(
        Order.id == int(order_id),
        Order.user_id == current_user.id,
    ).first()  # ← .first(), не .firts()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    # 4) Статус/сумма из сессии
    payment_status = getattr(session, "payment_status", None) or getattr(session, "status", "unknown")
    amount_total = (getattr(session, "amount_total", 0) or 0) / 100.0
    currency = (getattr(session, "currency", "usd") or "usd").upper()

    # 5) Обновляем заказ при успешной оплате
    if payment_status == "paid" and order.status != "Paid":
        order.status = "Paid"
        db.add(order)
        db.commit()
        db.refresh(order)

    return {
        "order": order,
        "payment_status": payment_status,
        "amount_total": amount_total,
        "currency": currency,
        "session_id": session_id,
    }