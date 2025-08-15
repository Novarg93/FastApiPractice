from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
import stripe

from app.database.session import get_db
from app.models.orders import Order
from app.models.users import User
from app.schemas.orders import OrderRead
from app.core.security import get_current_user

router = APIRouter()

class StripeSuccessResp(BaseModel):
    order: OrderRead
    payment_status: str
    amount_total: float
    currency: str
    session_id: str

@router.get("/stripe/success", response_model=StripeSuccessResp)
def stripe_success(
        session_id: str = Query(..., description="ID сессии Stripe Checkout"),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Stripe error: {e}")

        meta = getattr(session, "metadata", {}) or {}
        order_id = meta.get("order_id")
        if not order_id:
            raise HTTPException(status_code=404, detail=f"Stripe error: order_id missing")

        order = db.query(Order).filter(
            Order.user.id == current_user.id,
        ).firts()
        if not order:
            raise HTTPException(status_code=404, detail=f"Stripe error: order not found")

        payment_status = getattr(session, "payment_status", None) or getattr(session, "status", "unknown" )
        amount_total = (getattr(session, "amount_total", 0) or 0) / 100.0
        currency = (getattr(session, "currency", "usd") or "usd").upper()

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