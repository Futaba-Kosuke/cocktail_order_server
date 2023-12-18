import os
from dataclasses import dataclass, field
from typing import List, Optional, TypedDict

from supabase import Client, create_client

IngredientLogDbResType = TypedDict(
    "IngredientLogDbResType", {"unit": int, "amount": int}
)

IngredientDbResType = TypedDict(
    "IngredientDbResType",
    {
        "id": int,
        "name": str,
        "unit": int,
        "amount": int,
        "alc_percent": float,
        "ingredient_unit": int,
        "ingredient_amount": int,
        "ingredient_log": List[IngredientLogDbResType],
    },
)

OrderMenuDbResType = TypedDict(
    "OrderMenuDbResType",
    {
        "id": int,
        "name": str,
        "description": str,
        "image_url": str,
        "method": int,
        "style": int,
        "specials": int,
        "ingredients": List[IngredientDbResType],
    },
)


@dataclass
class SupabaseClient:
    supabase: Client = field(init=False)

    def __post_init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_API_KEY")
        self.supabase = create_client(url, key)

    def __self_menu_row_to_res(self, row):
        return {
            "id": row["id"],
            "name": row["name"],
            "image_url": row["image_url"],
            "alc_percent": row["alc_percent"],
        }

    def get_self_menu_list(self):
        res = self.supabase.table("self_menu").select("*").execute()
        return [self.__self_menu_row_to_res(row) for row in res.data]

    def __order_menu_row_to_res(self, row) -> OrderMenuDbResType:
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
                    "ingredient_amount": recipe["ingredient"]["amount"],
                    "ingredient_unit": recipe["ingredient"]["unit"],
                    "ingredient_log": [
                        {"unit": log["unit"], "amount": log["amount"]}
                        for log in recipe["ingredient"]["ingredient_log"]
                    ],
                }
                for recipe in row["recipe"]
            ],
        }

    def get_order_menu_list(self) -> List[OrderMenuDbResType]:
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
                        "recipe(ingredient(*, ingredient_log(unit, amount)), unit, amount)",
                    ]
                )
            )
            .execute()
        )
        return [self.__order_menu_row_to_res(row) for row in res.data]

    def get_order_menu(self, id: int) -> Optional[OrderMenuDbResType]:
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
                        "recipe(ingredient(*, ingredient_log(unit, amount)), unit, amount)",
                    ]
                )
            )
            .eq("id", id)
            .execute()
        )
        if res is None or res.data is None or len(res.data) == 0:
            return None

        return self.__order_menu_row_to_res(res.data[0])

    def get_ingredients(self):
        res = (
            self.supabase.table("ingredient")
            .select(
                ", ".join(
                    [
                        "id",
                        "name",
                        "unit",
                        "amount",
                        "alc_percent",
                        "ingredient_log(unit, amount)",
                    ]
                )
            )
            .execute()
        )
        if res is None or res.data is None:
            return []

        return res.data

    def get_ingredients_by_ids(self, ids: List[int]):
        res = (
            self.supabase.table("ingredient")
            .select(
                ", ".join(
                    [
                        "id",
                        "name",
                        "unit",
                        "amount",
                        "alc_percent",
                        "ingredient_log(unit, amount)",
                    ]
                )
            )
            .in_("id", ids)
            .execute()
        )
        if res is None or res.data is None:
            return []

        return res.data

    def insert_order_log(self, order_log, ingredient_log_list):
        order_log_res = (
            self.supabase.table("order_log").insert(order_log).execute()
        )
        if (
            order_log_res is None
            or order_log_res.data is None
            or len(order_log_res.data) == 0
        ):
            return None
        order_log_id = order_log_res.data[0]["id"]
        for ingredient_log in ingredient_log_list:
            ingredient_log["order_log_id"] = order_log_id
        self.supabase.table("ingredient_log").insert(
            ingredient_log_list
        ).execute()
        return order_log_id

    def get_order_log_by_statuses(self, target_statuses):
        res = (
            self.supabase.table("order_log")
            .select("id, order_menu(name), status, created_at")
            .in_("status", target_statuses)
            .execute()
        )
        return res.data

    def update_order_log(self, id: int, status: int):
        res = (
            self.supabase.table("order_log")
            .update({"status": status})
            .eq("id", id)
            .execute()
        )
        return res.data
