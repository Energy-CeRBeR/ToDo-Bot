from typing import Dict

start_text = f"""👋 Привет! Я *ToDo-Bot*, твой помощник для работы с сервисом [ToDo](https://energy-cerber.ru)

Здесь ты можешь управлять своими задачами, даже не заходя на сам сайт! 🤩

Чтобы авторизоваться, введите команду /auth
Для просмотра полного списка команд введите /help
  
Приятной работы! 😊
"""

help_text = """
*Список доступных команд* 📝

/start - начать работу с ToDo-Bot
/help - получить справку по доступным командам
/profile - просмотр аккаунта
/auth - авторизоваться
/logout - выйти из аккаунта
/categories - Просмотр списка созданных категорий задач
/all\_tasks - Просмотр списка всех созданных задач
/active\_tasks - Просмотр списка всех активных задач
/completed\_tasks - Просмотр списка всех выполненных задач
/create\_category - Создание новой категории задач
/create\_task - Создание новой задачи
"""


def parse_user_information(user_dict: Dict):
    profile_info = f"""
✅ *Вы успешно вошли!* ✅ 

**Имя:** *{user_dict["name"]}*
**Фамилия:** *{user_dict["surname"]}*
**Email:** *{user_dict["email"]}*
"""

    return profile_info


LEXICON_COMMANDS: dict = {
    "/start": start_text,
    "/help": help_text,
    "/auth": {
        "already_authorized": "Вы уже авторизованы! 😉",
        "not_authorized": "Введите почту, привязанную к сайту:"
    },
    "/profile": parse_user_information,
    "/logout": {
        "confirm": "❓ Вы действительно хотите выйти из аккаунта ❓",
        "already_logout": "Вход в аккаунт не был выполнен. Выход невозможен 🙂"
    }
}

LEXICON: dict[str, str] = {
    "get_password": "Введите пароль:",
    "not_auth": "Вы не авторизованны! 🙁\nВведите /auth для входа в аккаунт",
    "invalid_auth": "Неверная почта или пароль 🙁\nПопробуйте ещё раз!",
    "success_auth": "Вход успешно выполнен! ✅\nВведите /profile для просмотра Вашей информации",
    "success_logout": "Вы успешно вышли из аккаунта! ✅",
    "categories_button_text": "Список категорий 📋",
    "tasks_button_text": "Список задач 📋"
}
