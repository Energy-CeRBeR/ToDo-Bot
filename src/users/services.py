from typing import Optional, Dict

from httpx import AsyncClient
from src.database.repositories import UserRepository

repository = UserRepository()


class UserService:
    __client = AsyncClient(base_url="https://energy-cerber.ru/user")

    async def get_current_user(self, access_token: str) -> Optional[Dict]:
        response = await self.__client.get("/self", headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code == 200:
            return response.json()

    async def refresh_access(self, refresh_token: str):
        response = await self.__client.post("/refresh", headers={"Authorization": f"Bearer {refresh_token}"})
        if response.status_code == 200:
            return response.json()

    async def login_user(self, email: str, password: str) -> Optional[Dict]:
        response = await self.__client.post("/login", params={"email": email, "password": password})
        if response.status_code == 200:
            return response.json()
