from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.models.items import Item
from app.models.options import Option, OptionChoice


def apply_price_adj(price_adj: dict, value: int = 1):
    multiplier = 1.0
    abs_sum = 0.0  # Используем float, т.к. цена - float

    if not price_adj:
        return multiplier, abs_sum

    if "pct" in price_adj and price_adj["pct"] is not None:
        multiplier *= 1 + price_adj["pct"] / 100

    if "abs_cents" in price_adj and price_adj["abs_cents"] is not None:
        abs_sum += price_adj["abs_cents"] * value

    if "multiplier" in price_adj and price_adj["multiplier"] is not None:
        multiplier *= price_adj["multiplier"]

    return multiplier, abs_sum


def calculate_price(db: Session, product_id: int, quantity: int, selected_options: list):
    # Загружаем товар и его опции одним запросом
    item = db.query(Item).options(
        joinedload(Item.options).joinedload(Option.choices)
    ).filter(Item.id == product_id).first()

    if not item:
        raise ValueError("Товар не найден")

    # Исходная цена товара
    base_total = item.price * quantity
    total_multiplier = 1.0
    abs_sum = 0.0
    applied_options = {}

    # Получаем все опции для товара, чтобы было проще искать
    product_options_map = {opt.name: opt for opt in item.options}

    for selected_option in selected_options:
        key = selected_option["name"]
        selected_value = selected_option["value"]

        # Ищем опцию по её уникальному имени
        option = product_options_map.get(key)
        if not option:
            continue

        if option.type == "radio" or option.type == "select":
            # Ищем выбранный вариант в списке вариантов опции
            choice = next((c for c in option.choices if c.value == selected_value), None)

            if choice:
                m, a = apply_price_adj({
                    "pct": choice.pct,
                    "abs_cents": choice.abs_cents,
                    "multiplier": choice.multiplier
                })
                total_multiplier *= m
                abs_sum += a
                applied_options[key] = {"value": selected_value}

        elif option.type == "slider":
            try:
                # Значение слайдера должно быть числом
                slider_value = int(selected_value)

                # Применяем модификаторы цены, если они есть
                m, a = apply_price_adj({
                    "pct": 0,
                    "abs_cents": 0,
                    "multiplier": 1.0,
                }, value=slider_value)
                total_multiplier *= m
                abs_sum += a
                applied_options[key] = {"value": slider_value}

            except (ValueError, TypeError):
                # Пропускаем, если значение некорректно
                continue

    final_price = (base_total * total_multiplier) + abs_sum

    return {
        "product_id": product_id,
        "item_name": item.name,
        "unit_price": item.price,
        "quantity": quantity,
        "base_total": base_total,
        "final_price": final_price,
        "applied_options": applied_options
    }