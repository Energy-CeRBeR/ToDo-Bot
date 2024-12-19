from typing import Optional, Dict, List
from httpx import AsyncClient


class TaskService:
    def __init__(self):
        self.client = AsyncClient(base_url="https://api.energy-cerber.ru/tasks")

    async def get_all_tasks(self, access_token: str) -> Optional[List[Dict]]:
        response = await self.client.get("/", headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code == 200:
            return response.json()

    async def get_task_by_id(self, task_id: int, access_token: str) -> Optional[Dict]:
        response = await self.client.get(f"/{task_id}", headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code == 200:
            return response.json()

    async def create_task(self, data: Dict, access_token: str) -> Optional[Dict]:
        response = await self.client.post("/", json=data, headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code == 200:
            return response.json()

    async def edit_task(self, task_id: int, data: Dict, access_token: str) -> Optional[Dict]:
        response = await self.client.put(f"/{task_id}", json=data, headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code == 200:
            return response.json()

    async def change_task_status(self, task_id: int, access_token: str) -> Optional[Dict]:
        response = await self.client.put(
            f"/{task_id}/change_status", headers={"Authorization": f"Bearer {access_token}"}
        )
        if response.status_code == 200:
            return response.json()

    async def delete_task(self, task_id: int, access_token: str) -> Optional[Dict]:
        response = await self.client.delete(f"/{task_id}", headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code == 200:
            return response.json()
