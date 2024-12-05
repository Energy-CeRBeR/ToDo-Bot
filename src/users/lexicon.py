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
/auth - авторизоваться в ToDo
/logout - выйти из аккаунта ToDo
"""

LEXICON: dict[str, str] = {

}

LEXICON_COMMANDS: dict = {
    "/start": start_text,
    "/help": help_text
}
