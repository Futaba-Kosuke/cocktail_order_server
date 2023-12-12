from typing import List, Literal

from pydantic import BaseModel

from .enum import MethodType, OrderStatusType, StyleType, UnitType


class SelfMenuModel(BaseModel):
    id: int
    name: str
    image_url: str
    alc_percent: float


class IngredientModel(BaseModel):
    id: int
    name: str
    unit: UnitType
    amount: int


class OrderMenuModel(BaseModel):
    id: int
    name: str
    description: str
    image_url: str
    method: MethodType
    style: StyleType
    specials: List[str] = ["HOT", "SNOW_STYLE"]
    alc_percent: float
    ingredients: List[IngredientModel]


class IngredientStockModel(BaseModel):
    id: int
    name: str
    alc_percent: float
    unit: UnitType
    amount: int


class OrderSuccessModel(BaseModel):
    order_id: str


class OrderLogCallingModel(BaseModel):
    order_id: str
    menu_name: str
    status: OrderStatusType


class DefaultSuccessModel(BaseModel):
    resp: Literal["success"]
