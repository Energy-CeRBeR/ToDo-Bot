from typing import Optional, Dict
from httpx import AsyncClient


class CategoryService:
    def __init__(self):
        self.client = AsyncClient(base_url="https://energy-cerber.ru/categories")

    async def get_categories(self, access_token: str) -> Optional[Dict]:
        response = await self.client.get("/categories", headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code == 200:
            return response.json()

    async def get_category(self, category_id: int, access_token: str) -> Optional[Dict]:
        response = await self.client.get(
            f"/categories/{category_id}", headers={"Authorization": f"Bearer {access_token}"}
        )
        if response.status_code == 200:
            return response.json()

    async def create_category(self, body: dict, access_token: str) -> Optional[Dict]:
        response = await self.client.post(
            "/categories", json=body, headers={"Authorization": f"Bearer {access_token}"}
        )
        if response.status_code == 200:
            return response.json()

    async def edit_category(self, category_id: int, body: dict, access_token: str) -> Optional[Dict]:
        response = await self.client.put(
            f"/categories/{category_id}", json=body, headers={"Authorization": f"Bearer {access_token}"}
        )
        if response.status_code == 200:
            return response.json()

    async def delete_category(self, category_id: int, access_token: str) -> Optional[Dict]:
        response = await self.client.delete(
            f"/categories/{category_id}", headers={"Authorization": f"Bearer {access_token}"}
        )
        if response.status_code == 200:
            return response.json()
