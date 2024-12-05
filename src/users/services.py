from typing import Optional, Dict

from httpx import AsyncClient

from src.database.models import User
from src.database.repository import UserRepository


class UserService:
    def __init__(self):
        self.client = AsyncClient(base_url="https://energy-cerber.ru/user")

    async def get_tg_user_by_id(self, user_id: int) -> Optional[User]:
        return await UserRepository().get_user_by_id(user_id)

    async def create_tg_user(self, user_id: int, username: str, first_name: str, last_name: str) -> Optional[User]:
        return await UserRepository().create_user(user_id, username, first_name, last_name)

    async def get_current_user(self, access_token: str) -> Optional[Dict]:
        response = await self.client.get("/self", headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code == 200:
            return response.json()

    async def refresh_access(self, refresh_token: str):
        response = await self.client.post("/refresh", headers={"Authorization": f"Bearer {refresh_token}"})
        if response.status_code == 200:
            return response.json()

    async def login_user(self, user_id: int, email: str, password: str) -> Optional[Dict]:
        response = await self.client.post("/login", params={"email": email, "password": password})
        if response.status_code == 200:
            resp_dict = response.json()
            await UserRepository().refresh_tokens(user_id, resp_dict["access_token"], resp_dict["refresh_token"])

            return await self.get_current_user(resp_dict["access_token"])

    async def logout_user(self, user_id: int):
        await UserRepository().refresh_tokens(user_id, "default", "default")
