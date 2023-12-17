import os
from typing import List

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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
    calc_amount,
    calc_ingredient_stock_amount,
    calc_order_menu_stock_amount,
    method_enum,
    order_status_enum,
    special_elements,
    style_enum,
    unit_enum,
)
from database_client import SupabaseClient

# load enviroments
load_dotenv()

# create fastapi instance
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin for origin in os.environ.get("ALLOW_ORIGINS", "").split(",")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create supabase client instance
database_client = SupabaseClient()

# create special bitset map
special_bitset = Bitset(special_elements)


@app.get("/self_menu", response_model=List[SelfMenuModel])
def get_self_menu_list():
    self_menu: List[SelfMenuModel] = database_client.get_self_menu_list()
    return self_menu


@app.get("/order_menu", response_model=List[OrderMenuModel])
def get_order_menu_list():
    raw_order_menu_list = database_client.get_order_menu_list()
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
            "stock": min(
                [
                    calc_order_menu_stock_amount(
                        ingredient_stock_amount=calc_ingredient_stock_amount(
                            initial_amount=ingredient["ingredient_amount"],
                            unit=ingredient["ingredient_unit"],
                            ingredient_logs=ingredient["ingredient_log"],
                        ),
                        ingredient_unit=ingredient["unit"],
                        order_menu_amount=ingredient["amount"],
                        order_menu_unit=ingredient["unit"],
                    )
                    for ingredient in menu["ingredients"]
                ]
            ),
        }
        for menu in raw_order_menu_list
    ]
    return res_order_menu_list


@app.get("/order_menu/{order_menu_id}", response_model=OrderMenuModel)
def get_order_menu_by_id(order_menu_id: int):
    raw_order_menu = database_client.get_order_menu(order_menu_id)
    if raw_order_menu is None:
        raise HTTPException(status_code=404, detail="Not Found...")
    res_order_menu = {
        "id": raw_order_menu["id"],
        "name": raw_order_menu["name"],
        "description": raw_order_menu["description"],
        "image_url": raw_order_menu["image_url"],
        "method": method_enum[raw_order_menu["method"]],
        "style": style_enum[raw_order_menu["style"]],
        "alc_percent": calc_alc_percent(raw_order_menu["ingredients"]),
        "specials": special_bitset.decimal_to_list(raw_order_menu["specials"]),
        "ingredients": [
            {
                "id": ingredient["id"],
                "name": ingredient["name"],
                "unit": unit_enum[ingredient["unit"]],
                "amount": ingredient["amount"],
            }
            for ingredient in raw_order_menu["ingredients"]
        ],
        "stock": min(
            [
                calc_order_menu_stock_amount(
                    ingredient_stock_amount=calc_ingredient_stock_amount(
                        initial_amount=ingredient["ingredient_amount"],
                        unit=ingredient["ingredient_unit"],
                        ingredient_logs=ingredient["ingredient_log"],
                    ),
                    ingredient_unit=ingredient["unit"],
                    order_menu_amount=ingredient["amount"],
                    order_menu_unit=ingredient["unit"],
                )
                for ingredient in raw_order_menu["ingredients"]
            ]
        ),
    }
    return res_order_menu


@app.get("/ingredient/stock", response_model=List[IngredientStockModel])
def get_ingredient_stock():
    raw_ingredients = database_client.get_ingredients()
    res_ingredient_stock = [
        {
            "id": ingredient["id"],
            "name": ingredient["name"],
            "alc_percent": ingredient["alc_percent"],
            "unit": unit_enum[ingredient["unit"]],
            "amount": calc_ingredient_stock_amount(
                initial_amount=ingredient["amount"],
                unit=ingredient["unit"],
                ingredient_logs=ingredient["ingredient_log"],
            ),
        }
        for ingredient in raw_ingredients
    ]
    return res_ingredient_stock


@app.post("/order/{order_menu_id}", response_model=OrderSuccessModel)
def order(order_menu_id: int):
    raw_order_menu = database_client.get_order_menu(order_menu_id)
    if raw_order_menu is None:
        raise HTTPException(status_code=404, detail="Not Found...")
    stock = min(
        [
            calc_order_menu_stock_amount(
                ingredient_stock_amount=calc_ingredient_stock_amount(
                    initial_amount=ingredient["ingredient_amount"],
                    unit=ingredient["ingredient_unit"],
                    ingredient_logs=ingredient["ingredient_log"],
                ),
                ingredient_unit=ingredient["unit"],
                order_menu_amount=ingredient["amount"],
                order_menu_unit=ingredient["unit"],
            )
            for ingredient in raw_order_menu["ingredients"]
        ]
    )
    if stock <= 0:
        raise HTTPException(status_code=400, detail="Bad Request...")

    # create logs
    order_log = {
        "status": order_status_enum.index("processing"),
        "order_menu_id": order_menu_id,
    }
    ingredient_log_list = [
        {
            "ingredient_id": ingredient["id"],
            "unit": ingredient["unit"],
            "amount": ingredient["amount"],
        }
        for ingredient in raw_order_menu["ingredients"]
    ]
    order_log_id = database_client.insert_order_log(
        order_log=order_log, ingredient_log_list=ingredient_log_list
    )
    return {"order_id": order_log_id}


@app.post("/manual_order", response_model=OrderSuccessModel)
def manual_order(manual_order: ManualOrderRequestModel):
    # check request payload
    req_ingredients = {
        ingredient.ingredient_id: {
            "unit": ingredient.unit,
            "amount": ingredient.amount,
        }
        for ingredient in manual_order.ingredients
    }
    raw_ingredients = database_client.get_ingredients_by_ids(
        list(req_ingredients.keys())
    )
    if raw_ingredients is None:
        raise HTTPException(status_code=404, detail="Not Found...")

    # check stock
    min_stock = min(
        [
            calc_ingredient_stock_amount(
                initial_amount=raw_ingredient["amount"],
                unit=raw_ingredient["unit"],
                ingredient_logs=raw_ingredient["ingredient_log"],
            )
            - calc_amount(
                amount=req_ingredients[raw_ingredient["id"]]["amount"],  # type: ignore
                unit=req_ingredients[raw_ingredient["id"]]["unit"],  # type: ignore
            )
            for raw_ingredient in raw_ingredients
        ]
    )
    if min_stock <= 0:
        raise HTTPException(status_code=400, detail="Bad Request...")

    # create logs
    order_log = {
        "status": order_status_enum.index("processing"),
    }
    ingredient_log_list = [
        {
            "ingredient_id": ingredient.ingredient_id,
            "unit": unit_enum.index(ingredient.unit),
            "amount": ingredient.amount,
        }
        for ingredient in manual_order.ingredients
    ]
    order_log_id = database_client.insert_order_log(
        order_log=order_log, ingredient_log_list=ingredient_log_list
    )
    return {"order_id": order_log_id}


@app.get("/order_log/display", response_model=List[OrderLogCallingModel])
def mock_get_display_order_log():
    order_log_list = database_client.get_order_log_by_statuses(
        [
            order_status_enum.index("processing"),
            order_status_enum.index("calling"),
        ]
    )
    return [
        {
            "order_id": order_log["id"],
            "menu_name": order_log["order_menu"]["name"]
            if order_log["order_menu"] is not None
            else "Order Made",
            "status": order_status_enum[order_log["status"]],
        }
        for order_log in order_log_list
    ]


@app.put(
    "/order_log/to_calling/{order_log_id}", response_model=DefaultSuccessModel
)
def mock_to_calling(order_log_id: int):
    return {"resp": "success"}


@app.put(
    "/order_log/to_complete/{order_log_id}", response_model=DefaultSuccessModel
)
def mock_to_complete_order(order_log_id: int):
    return {"resp": "success"}


def main() -> None:
    print("===== main() =====")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2)


if __name__ == "__main__":
    main()
