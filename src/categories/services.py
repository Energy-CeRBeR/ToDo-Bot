from typing import Optional, Dict, List
from httpx import AsyncClient


class CategoryService:
    def __init__(self):
        self.client = AsyncClient(base_url="https://energy-cerber.ru/api/v1/categories")

    async def get_categories(self, access_token: str) -> Optional[List[Dict]]:
        response = await self.client.get("/", headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code == 200:
            return response.json()

    async def get_category(self, category_id: int, access_token: str) -> Optional[Dict]:
        response = await self.client.get(f"/{category_id}", headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code == 200:
            return response.json()

    async def create_category(self, name: str, color: str, access_token: str) -> Optional[Dict]:
        response = await self.client.post("/", json={"name": name, "color": color},
                                          headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code == 200:
            return response.json()

    async def edit_category(self, category_id: int, body: dict, access_token: str) -> Optional[Dict]:
        response = await self.client.put(
            f"/{category_id}", json=body, headers={"Authorization": f"Bearer {access_token}"}
        )
        if response.status_code == 200:
            return response.json()

    async def delete_category(self, category_id: int, access_token: str) -> Optional[Dict]:
        response = await self.client.delete(f"/{category_id}", headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code == 200:
            return response.json()
