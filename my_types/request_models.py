from typing import List, Literal

from pydantic import BaseModel


class IngredientRequestModel(BaseModel):
    liquid_id: int
    unit: Literal["ml", "tea_spoon", "dash"]
    amount: int


class ManualOrderRequestModel(BaseModel):
    ingredients: List[IngredientRequestModel]
