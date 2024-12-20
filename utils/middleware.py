from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.users.services import UserService
from src.users.lexicon import LEXICON as USER_LEXICON

user_service = UserService()


class AuthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        state = data['state']
        user_data = await state.get_data()
        user_dict = await user_service.get_current_user(user_data.setdefault("access_token", "default"))

        if not user_dict:
            refresh_tokens = await user_service.refresh_access(user_data.setdefault("refresh_token", "default"))
            if refresh_tokens is not None:
                await state.update_data(
                    access_token=refresh_tokens["access_token"],
                    refresh_token=refresh_tokens["refresh_token"]
                )
            else:
                await event.answer(text=USER_LEXICON["not_auth"])
                return 0

        return await handler(event, data)
