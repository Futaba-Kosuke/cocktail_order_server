from .enum import UnitType, unit_enum


def calc_alc_percent(ingredients) -> float:
    if len(ingredients) == 0:
        return 0

    numerator = sum(
        [
            ingredient["alc_percent"] * ingredient["amount"]
            for ingredient in ingredients
            if unit_enum[ingredient["unit"]] == "ml"
        ]
    )
    denominator = sum(
        [
            ingredient["amount"]
            for ingredient in ingredients
            if unit_enum[ingredient["unit"]] == "ml"
        ]
    )
    return round(numerator / denominator, 1)


def calc_ingredient_stock_amount(
    initial_amount: int,
    unit: int,
    ingredient_logs,
) -> int:
    if unit_enum[unit] == "ml":
        amount = initial_amount
        for log in ingredient_logs:
            log_unit: str = unit_enum[log["unit"]]
            if log_unit == "ml" or log_unit == "dash":
                amount = amount - log["amount"]
            elif log_unit == "tea_spoon":
                amount = amount - log["amount"] * 5
        return amount
    elif unit_enum[unit] == "slice":
        return initial_amount - sum(
            [
                log["amount"]
                for log in ingredient_logs
                if unit_enum[log["unit"]] == "slice"
            ]
        )
    return initial_amount


def calc_order_menu_stock_amount(
    ingredient_stock_amount: int,
    ingredient_unit: int,
    order_menu_amount: int,
    order_menu_unit: int,
) -> int:
    if (
        unit_enum[ingredient_unit] == "ml"
        and unit_enum[order_menu_unit] == "tea_spoon"
    ):
        return int(ingredient_stock_amount / (order_menu_amount * 5))
    return int(ingredient_stock_amount / order_menu_amount)


def calc_amount(amount: int, unit: UnitType) -> int:
    if unit == "tea_spoon":
        return amount * 5
    if unit == "drop":
        return 0
    return amount
