from typing import List

from pydantic import BaseModel

from .enum import UnitType


class IngredientRequestModel(BaseModel):
    ingredient_id: int
    unit: UnitType
    amount: int


class ManualOrderRequestModel(BaseModel):
    ingredients: List[IngredientRequestModel]
