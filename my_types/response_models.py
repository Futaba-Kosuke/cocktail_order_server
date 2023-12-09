from typing import List, Literal

from pydantic import BaseModel


class IngredientModel(BaseModel):
    id: int
    name: str
    unit: Literal["ml", "tea_spoon", "dash"]
    amount: int


class MenuModel(BaseModel):
    id: int
    name: str
    description: str
    image_url: str
    method: Literal["stir", "shake", "build"]
    style: Literal["short", "long"]
    specials: List[str] = ["HOT", "SNOW_STYLE"]
    alc_percent: float
    ingredients: List[IngredientModel]


class LiquidStockModel(BaseModel):
    id: int
    name: str
    alc_percent: float
    amount_ml: int


class OrderSuccessModel(BaseModel):
    order_id: str
