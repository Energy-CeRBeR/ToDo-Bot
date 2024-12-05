from typing import Dict

start_text = f"""👋 Привет! Я ToDo-Bot, твой помощник для работы с сервисом [ToDo](https://energy-cerber.ru)
Здесь ты можешь управлять своими задачами, даже не заходя на сам сайт! 🤩

Чтобы авторизоваться, введите команду /auth
Для просмотра полного списка команд введите /help
  
Приятной работы! 😊
"""

help_text = """
Список доступных команд:

/start - начать работу с ToDo-Bot
/help - получить справку по доступным командам
/profile - перейти в свой аккаунт
/auth - авторизоваться
/logout - выйти из аккаунта
"""


def parse_user_information(user_dict: Dict):
    # Создать функцию для вывода информации о пользователе в разделе профиль
    pass


LEXICON_COMMANDS: dict = {
    "/start": start_text,
    "/help": help_text,
    "/auth": {
        "already_authorized": "Вы уже авторизованы! 😉",
        "not_authorized": "Введите почту, привязанную к сайту:"
    }
}

LEXICON: dict[str, str] = {
    "get_password": "Введите пароль:",
    "invalid_auth": "Неверная почта или пароль 🙁 Попробуйте ещё раз!",
    "success_auth": "Вход успешно выполнен!",
    "categories_button_text": "Список категорий 📋",
    "tasks_button_text": "Список задач 📋"
}
