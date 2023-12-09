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
