from sqlalchemy.orm import Session
from app.models.items import Item


def apply_price_adj(price_adj: dict, value: int = 1):
    multiplier = 1.0
    abs_sum = 0

    if not price_adj:
        return multiplier, abs_sum

    order = price_adj['order']

    if order == "pctThenAbs":
        if "pct" in price_adj and price_adj["pct"] is not None:
            multiplier *= 1 + price_adj["pct"]
        if "absCents" in price_adj and price_adj["absCents"] is not None:
            abs_sum += price_adj["absCents"] * value

    elif order == "absThenPct":
        if "absCents" in price_adj and price_adj["absCents"] is not None:
            abs_sum += price_adj["absCents"] * value
        if "pct" in price_adj and price_adj["pct"] is not None:
            multiplier *= 1 + price_adj["pct"]

    else:
        if "pct" in price_adj and price_adj["pct"] is not None:
            multiplier *= 1 + price_adj["pct"]
        if "absCents" in price_adj and price_adj["absCents"] is not None:
            abs_sum += price_adj["absCents"] * value

    if "multiplier" in price_adj and price_adj["multiplier"] is not None:
        multiplier *= 1 + price_adj["multiplier"]

    return multiplier, abs_sum


def calculate_price(
        db: Session,
        product_id: int,
        quantity: int,
        selections: dict,
        product_options: list[dict],
) -> dict:

    item = db.query(Item).filter(Item.id == product_id).first()
    if not item:
        raise ValueError("Product not found")

    unit_price = item.price
    item_name = item.name

    base_total = unit_price * quantity

    total_multiplier = 1.0
    abs_sum = 0
    applied_options = {}

    #### All Options ####
    for option in product_options:
        key = option["key"]
        selected = selections.get(key)

        #### Radio / Select ####
        if option["type"] in ("radio", "select") and isinstance(selected, str):
            choice = next((c for c in option["choices"] if c["value"] == selected), None)
            if choice and "price" in choice:
                m, a = apply_price_adj(choice["price"])
                total_multiplier *= m
                abs_sum += a
                applied_options[key] = {"value": selected, **choice["price"]}

        #### CheckBoxes ####
        elif option["type"] == "checkboxes" and isinstance(selected, list):
            applied_options[key] = []
            for val in selected:
                choice = next((c for c in option["choices"] if c["value"] == val), None)
                if choice and "price" in choice:
                    m, a = apply_price_adj(choice["price"])
                    total_multiplier *= m
                    abs_sum += a
                    applied_options[key].append({"value": val, **choice["price"]})

        #### Slider / Number ####
        elif option["type"] in ("slider", "number") and isinstance(selected, int):
            pricing = option.get("pricing")
            if pricing:
                if pricing["mode"] == "per_unit":
                    m, a = apply_price_adj(pricing.get("perUnit"), selected)
                    abs_sum += a
                    applied_options[key] = {"value": selected, **(pricing.get("perUnit", {}))}
                elif pricing["mode"] == "tiered":
                    tier = next((t for t in pricing["tiers"] if selected <= t["upTo"]), None)
                    if tier and "price" in tier:
                        m, a = apply_price_adj(tier["price"])
                        total_multiplier *= m
                        abs_sum += a
                        applied_options[key] = {"value": selected, **tier["price"]}

    final_price = int((base_total * total_multiplier) + abs_sum)

    return {
        "product_id": product_id,
        "item_name": item_name,
        "unit_price": unit_price,
        "quantity": quantity,
        "base_total": base_total,
        "options": applied_options,
        "final_price": final_price,
    }
