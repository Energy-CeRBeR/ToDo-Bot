import asyncio

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import Config, load_config
from src.users.handlers import router as user_router
from src.categories.handlers import router as category_router
from src.tasks.handlers import router as task_router


async def main():
    config: Config = load_config(".env")
    bot = Bot(token=config.tg_bot.token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(user_router)
    dp.include_router(category_router)
    dp.include_router(task_router)

    print("Starting!")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
