from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils.middleware import AuthMiddleware
from .services import CategoryService

router = Router()
router.message.middleware(AuthMiddleware())
category_service = CategoryService()


@router.message(Command(commands="categories"))
async def get_categories(message: Message):
    await message.answer("Categories")
