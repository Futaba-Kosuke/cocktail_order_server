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
