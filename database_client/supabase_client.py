import os
from dataclasses import dataclass, field

from supabase import Client, create_client


@dataclass
class SupabaseClient:
    supabase: Client = field(init=False)

    def __post_init__(self):
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_API_KEY")
        self.supabase = create_client(url, key)

    def __self_menu_row_to_res(row):
        return {
            "id": row["id"],
            "name": row["name"],
            "image_url": row["image_url"],
            "alc_percent": row["alc_percent"],
        }

    def get_self_menu_list(self):
        res = self.supabase.table("self_menu").select("*").execute()
        return [self.__self_menu_row_to_res(row) for row in res.data]

    def __order_menu_row_to_res(self, row):
        return {
            "id": row["id"],
            "name": row["name"],
            "description": row["description"],
            "image_url": row["image_url"],
            "method": row["method"],
            "style": row["style"],
            "specials": row["specials"],
            "ingredients": [
                {
                    "id": recipe["ingredient"]["id"],
                    "name": recipe["ingredient"]["name"],
                    "unit": recipe["unit"],
                    "amount": recipe["amount"],
                    "alc_percent": recipe["ingredient"]["alc_percent"],
                }
                for recipe in row["recipe"]
            ],
        }

    def get_order_menu_list(self):
        res = (
            self.supabase.table("order_menu")
            .select(
                ", ".join(
                    [
                        "id",
                        "name",
                        "description",
                        "image_url",
                        "method",
                        "style",
                        "specials",
                        "recipe(ingredient(*), unit, amount)",
                    ]
                )
            )
            .execute()
        )
        return [self.__order_menu_row_to_res(row) for row in res.data]

    def get_order_menu(self, id: int):
        res = (
            self.supabase.table("order_menu")
            .select(
                ", ".join(
                    [
                        "id",
                        "name",
                        "description",
                        "image_url",
                        "method",
                        "style",
                        "specials",
                        "recipe(ingredient(*), unit, amount)",
                    ]
                )
            )
            .eq("id", id)
            .execute()
        )
        if res is None or res.data is None or len(res.data) == 0:
            return None

        return self.__order_menu_row_to_res(res.data[0])

    def get_ingredient_stock(self):
        res = (
            self.supabase.table("ingredient")
            .select(
                ", ".join(
                    [
                        "id",
                        "name",
                        "alc_percent",
                        "unit",
                        "amount",
                        "ingredient_log(unit, amount)",
                    ]
                )
            )
            .execute()
        )
        if res is None or res.data is None:
            return []

        return res.data
