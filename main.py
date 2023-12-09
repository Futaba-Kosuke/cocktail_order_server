from typing import List

import uvicorn
from fastapi import FastAPI

from my_types import LiquidStockModel, MenuModel, SuccessModel

app = FastAPI()


@app.get("/menu", response_model=List[MenuModel])
def get_menu_list():
    return [
        {
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
    ]


@app.get("/menu/{menu_id}", response_model=MenuModel)
def get_menu_by_id(menu_id: int):
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


@app.get("/liquid/stock", response_model=List[LiquidStockModel])
def get_liquid_stock():
    return [
        {
            "id": 1,
            "name": "ウィスキー",
            "alc_percent": 40,
            "amount_ml": 1000,
        },
        {
            "id": 2,
            "name": "スイートベルモット",
            "alc_percent": 16,
            "amount_ml": 1000,
        },
        {
            "id": 3,
            "name": "アロマティックビダーズ",
            "alc_percent": 0,
            "amount_ml": 100,
        },
    ]


@app.post("/order/{menu_id}", response_model=SuccessModel)
def order(menu_id: int):
    return {"resp": "success"}


def main() -> None:
    print("===== main() =====")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2)


if __name__ == "__main__":
    main()
