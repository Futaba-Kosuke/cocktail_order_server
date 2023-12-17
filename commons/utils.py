from typing import Dict, List

from .enum import unit_enum


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
    initial_amount: int, unit: int, ingredient_logs: List[Dict[str, int]]
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
