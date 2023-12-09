from typing import List, Literal

from pydantic import BaseModel


class SelfMenuModel(BaseModel):
    id: int
    name: str
    image_url: str
    alc_percent: float


class IngredientModel(BaseModel):
    id: int
    name: str
    unit: Literal["ml", "tea_spoon", "dash", "slice"]
    amount: int


class OrderMenuModel(BaseModel):
    id: int
    name: str
    description: str
    image_url: str
    method: Literal["stir", "shake", "build"]
    style: Literal["short", "long"]
    specials: List[str] = ["HOT", "SNOW_STYLE"]
    alc_percent: float
    ingredients: List[IngredientModel]


class IngredientStockModel(BaseModel):
    id: int
    name: str
    alc_percent: float
    unit: Literal["ml", "tea_spoon", "dash", "slice"]
    amount: int


class OrderSuccessModel(BaseModel):
    order_id: str


class OrderLogCallingModel(BaseModel):
    order_id: str
    menu_name: str
    status: Literal["processing", "calling"]


class DefaultSuccessModel(BaseModel):
    resp: Literal["success"]
