task_about_text = """
Название: *{name}*

Описание: _{description}_

Приоритет: *{priority}*

Категория: *{category}*

Состояние: *{status}*

Дата: *{date}*
"""

LEXICON: dict = {
    "get_name": "Введите название задачи: ",
    "get_description": "Введите описание задачи: ",
    "get_priority": "Выберите приоритет задачи: ",
    "get_date": "Выберите дату задачи: ",
    "get_year": "Введите год: ",
    "get_month": "Введите месяц: ",
    "successful_create": "Задача успешно создана! ✅️",
    "no_add_description": "Не добавлять описание ❌",
    "low_priority": "Низкий",
    "medium_priority": "Средний",
    "high_priority": "Высокий",
    "prev_calendar_page": "<<<<",
    "next_calendar_page": ">>>>",
    "tasks_menu": "Выберите действие: ",
    "tasks_today": "Задачи на сегодня",
    "tasks_from_day": "Выбрать день для просмотра",
    "all_tasks": "Просмотр всех задач",
    "active_tasks": "Просмотр активных задач",
    "completed_tasks": "Просмотр выполненных задач",
    "show_tasks_from_day": "Список задач на {date}",
    "show_task_about": task_about_text,
    "no_description": "Без описания",
    "edit_task": "Изменить задачу ✏️",
    "edit_status": ["Пометить выполненной ✅️", "Отменить выполнение ❌"],
    "delete_task": "Удалить задачу ❌",
    "check_status": ["Не выполнена ❌", "Выполнена ✅️"],
    "task_status_changed": "Статус задачи успешно изменён! ✅️",
    "delete_task_confirmation": "❓ Вы действительно хотите удалить данную задачу ❓",
    "cancel_delete": "Операция удаления отменена!",
    "task_deleted": "Задача успешно удалена! ✅️",
}

LEXICON_COMMANDS: dict = {
    "/all_tasks": "Список всех задач, отсортированный по дате создания📋",
    "/active_tasks": "Список активных задач, отсортированный по дате создания 📋",
    "/completed_tasks": "Список выполненных задач, отсортированный по дате создания 📋",
    "/create_task": "Выберите категорию для задачи:"
}
