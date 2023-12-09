from typing import List

import uvicorn
from fastapi import FastAPI

from my_types import MenuModel

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
                {"id": 1, "name": "ウィスキー", "unit": "ml", "amount_ml": 45,},
                {"id": 2, "name": "スイートベルモット", "unit": "ml", "amount_ml": 15,},
                {
                    "id": 3,
                    "name": "アロマティックビダーズ",
                    "unit": "dash",
                },
            ],
        }
    ]



def main() -> None:
    print("===== main() =====")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2)


if __name__ == "__main__":
    main()
