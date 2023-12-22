from .enum import UnitType, unit_enum


def calc_alc_percent(ingredients, glass_ml: int) -> float:
    if len(ingredients) == 0:
        return 0

    numerator = sum(
        [
            ingredient["alc_percent"] * ingredient["amount"]
            if unit_enum[ingredient["unit"]] == "ml"
            or unit_enum[ingredient["unit"]] == "dash"
            else ingredient["alc_percent"] * ingredient["amount"] * 5
            if unit_enum[ingredient["unit"]] == "tea_spoon"
            else ingredient["alc_percent"]
            * calc_any(
                ingredient["amount"],
                glass_ml,
                ingredients,
            )
            for ingredient in ingredients
            if unit_enum[ingredient["unit"]] != "drop"
            and unit_enum[ingredient["unit"]] != "slice"
        ]
    )
    denominator = sum(
        [
            ingredient["amount"]
            if unit_enum[ingredient["unit"]] == "ml"
            or unit_enum[ingredient["unit"]] == "dash"
            else ingredient["amount"] * 5
            if unit_enum[ingredient["unit"]] == "tea_spoon"
            else calc_any(
                ingredient["amount"],
                glass_ml,
                ingredients,
            )
            for ingredient in ingredients
            if unit_enum[ingredient["unit"]] != "drop"
            and unit_enum[ingredient["unit"]] != "slice"
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
    if unit == "drop" or unit == "any":
        return 0
    return amount


def calc_any(amount: int, glass_ml: int, ingredients) -> int:
    return glass_ml - sum(
        [
            calc_amount(
                amount=ingredient["amount"], unit=unit_enum[ingredient["unit"]]
            )
            for ingredient in ingredients
            if unit_enum[ingredient["unit"]] != "slice"
        ]
    )
