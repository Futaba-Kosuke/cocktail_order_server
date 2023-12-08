from typing import List, Literal, Union

from pydantic import BaseModel


class IngredientModel(BaseModel):
    id: int
    name: str
    unit: Literal["ml", "tea_spoon", "dash"]
    amount_ml: Union[int, None] = None


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
