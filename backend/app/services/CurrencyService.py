from sqlalchemy.orm import Session
from app.models.items import Item
from app.core.pricing import OPTION_PRICE_RULES

def calculate_price(db: Session, product_id: int, quantity: int, selected_options: list[dict]) -> dict:
    item = db.query(Item).filter(Item.id == product_id).first()
    if not item:
        raise ValueError("Product not found")

    unit_price = item.price
    item_name = item.name

    base_total = unit_price * quantity

    total_multiplier = 1.0
    applied_options = {}

    for option in selected_options:
        name = option.get("name")
        value = option.get("value")

        if name in OPTION_PRICE_RULES and value in OPTION_PRICE_RULES[name]:
            percent = OPTION_PRICE_RULES[name][value]
            total_multiplier *= percent
            applied_options[name] = {"value": value, "percent": percent}
        else:
            applied_options[name] = {"value": value, "percent": 0.0}
    final_price = base_total * total_multiplier
    return {
        "product_id": product_id,
        "item_name": item_name,
        "unit_price": unit_price,
        "quantity": quantity,
        "base_total": round(base_total, 2),
        "options": applied_options,
        "final_price": round(final_price, 2),
    }