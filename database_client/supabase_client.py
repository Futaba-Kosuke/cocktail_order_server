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

    def get_self_menu_list(self):
        res = self.supabase.table("self_menu").select("*").execute()
        return [
            {
                "id": row["id"],
                "name": row["name"],
                "image_url": row["image_url"],
                "alc_percent": row["alc_percent"],
            }
            for row in res.data
        ]

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
        print(res)

        return [
            {
                "id": order_menu["id"],
                "name": order_menu["name"],
                "description": order_menu["description"],
                "image_url": order_menu["image_url"],
                "method": order_menu["method"],
                "style": order_menu["style"],
                "specials": order_menu["specials"],
                "ingredients": [
                    {
                        "id": recipe["ingredient"]["id"],
                        "name": recipe["ingredient"]["name"],
                        "unit": recipe["unit"],
                        "amount": recipe["amount"],
                        "alc_percent": recipe["ingredient"]["alc_percent"],
                    }
                    for recipe in order_menu["recipe"]
                ],
            }
            for order_menu in res.data
        ]
