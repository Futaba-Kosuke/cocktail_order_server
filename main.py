from typing import List

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from commons import (
    Bitset,
    DefaultSuccessModel,
    IngredientStockModel,
    ManualOrderRequestModel,
    OrderLogCallingModel,
    OrderMenuModel,
    OrderSuccessModel,
    SelfMenuModel,
    calc_alc_percent,
    method_enum,
    special_elements,
    style_enum,
    unit_enum,
)
from database_client import SupabaseClient

# load enviroments
load_dotenv()

# create fastapi instance
app = FastAPI()

# create supabase client instance
database_client = SupabaseClient()


@app.get("/self_menu", response_model=List[SelfMenuModel])
def get_self_menu_list():
    self_menu: List[SelfMenuModel] = database_client.get_self_menu_list()
    return self_menu


@app.get("/order_menu", response_model=List[OrderMenuModel])
def get_order_menu_list():
    raw_order_menu_list = database_client.get_order_menu_list()

    special_bitset = Bitset(special_elements)
    res_order_menu_list = [
        {
            "id": menu["id"],
            "name": menu["name"],
            "description": menu["description"],
            "image_url": menu["image_url"],
            "method": method_enum[menu["method"]],
            "style": style_enum[menu["style"]],
            "alc_percent": calc_alc_percent(menu["ingredients"]),
            "specials": special_bitset.decimal_to_list(menu["specials"]),
            "ingredients": [
                {
                    "id": ingredient["id"],
                    "name": ingredient["name"],
                    "unit": unit_enum[ingredient["unit"]],
                    "amount": ingredient["amount"],
                }
                for ingredient in menu["ingredients"]
            ],
        }
        for menu in raw_order_menu_list
    ]
    return res_order_menu_list


@app.get("/order_menu/{order_menu_id}", response_model=OrderMenuModel)
def get_order_menu_by_id(order_menu_id: int):
    return {
        "id": 1,
        "name": "マンハッタン",
        "description": "マンハッタン（英: Manhattan）は、ウイスキーベースのカクテルの一種である。カクテルの女王と呼ばれる",
        "image_url": "https://liqul.com/upimg/2020/06/015-manhattan01.jpg",
        "method": "stir",
        "style": "short",
        "specials": [],
        "alc_percent": 34.0,
        "ingredients": [
            {
                "id": 1,
                "name": "ウィスキー",
                "unit": "ml",
                "amount": 45,
            },
            {
                "id": 2,
                "name": "スイートベルモット",
                "unit": "ml",
                "amount": 15,
            },
            {
                "id": 3,
                "name": "アロマティックビダーズ",
                "unit": "dash",
                "amount": 1,
            },
        ],
    }


@app.get("/ingredient/stock", response_model=List[IngredientStockModel])
def get_ingredient_stock():
    return [
        {
            "id": 1,
            "name": "ウィスキー",
            "alc_percent": 40,
            "unit": "ml",
            "amount": 1000,
        },
        {
            "id": 2,
            "name": "スイートベルモット",
            "alc_percent": 16,
            "unit": "ml",
            "amount": 1000,
        },
        {
            "id": 3,
            "name": "アロマティックビダーズ",
            "alc_percent": 0,
            "unit": "ml",
            "amount": 100,
        },
        {
            "id": 4,
            "name": "レモン",
            "alc_percent": 0,
            "unit": "slice",
            "amount": 24,
        },
    ]


@app.post("/order/{order_menu_id}", response_model=OrderSuccessModel)
def order(order_menu_id: int):
    return {"order_id": 1}


@app.post("/order/manual", response_model=OrderSuccessModel)
def manual_order(manual_order: ManualOrderRequestModel):
    return {"order_id": 1}


@app.get("/order_log/display", response_model=List[OrderLogCallingModel])
def get_display_order_log():
    return [
        {
            "order_id": 1,
            "menu_name": "マンハッタン",
            "status": "processing",
        },
        {
            "order_id": 2,
            "menu_name": "ほげカクテル",
            "status": "processing",
        },
        {
            "order_id": 3,
            "menu_name": "ふがカクテル",
            "status": "calling",
        },
    ]


@app.put(
    "/order_log/complete/{order_log_id}", response_model=DefaultSuccessModel
)
def complete_order(order_log_id: int):
    return {"resp": "success"}


def main() -> None:
    print("===== main() =====")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2)


if __name__ == "__main__":
    main()
