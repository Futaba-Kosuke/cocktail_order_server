from typing import List, Literal

from pydantic import BaseModel


class IngredientRequestModel(BaseModel):
    ingredient_id: int
    unit: Literal["ml", "tea_spoon", "dash", "slice"]
    amount: int


class ManualOrderRequestModel(BaseModel):
    ingredients: List[IngredientRequestModel]
