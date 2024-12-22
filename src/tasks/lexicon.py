from typing import Dict

from utils.utils import inverse_priority_converter

task_about_text = """
Название: *{name}*

Описание: _{description}_

Приоритет: *{priority}*

Категория: *{category}*

Состояние: *{status}*

Дата: *{date}*
"""


def create_task_about_text(task: Dict, task_category: Dict):
    name = task["name"]
    description = task["description"] if task["description"] else LEXICON["no_description"]
    priority = inverse_priority_converter[task["priority"]]
    category = task_category["name"]
    status = LEXICON["check_status"][int(task["completed"])]
    date = task["date"]

    return task_about_text.format(
        name=name, description=description, priority=priority, category=category, status=status, date=date
    )


LEXICON: dict = {
    "get_name": "Введите название задачи: ",
    "get_description": "Введите описание задачи: ",
    "get_priority": "Выберите приоритет задачи: ",
    "get_date": "Выберите дату задачи: ",
    "get_year": "Введите год: ",
    "get_month": "Введите месяц: ",
    "get_category": "Выберите категорию для задачи.\nСтраница {page} / {pages}",
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
    "edit_name": "Изменить название задачи",
    "edit_description": "Изменить описание задачи",
    "edit_priority": "Изменить приоритет задачи",
    "edit_category": "Изменить категорию задачи",
    "edit_date": "Изменить дату задачи",
    "back_to_task": "⏪ Вернуться к просмотру задачи",
    "edit_task_menu": "Что вы хотите изменить?",
    "name_edited": "Название задачи успешно обновлено! ✅️",
    "description_edited": "Описание задачи успешно обновлено! ✅",
    "priority_edited": "Приоритет задачи успешно обновлён! ✅",
    "category_edited": "Категория задачи успешно обновлена! ✅",
    "date_edited": "Дата задачи успешно обновлена! ✅",
    "tasks_from_category": "Список задач из категории *{name}*\nСтраница {page} / {pages}",
    "error_state": "Вы не завершили какой-то процесс в окне с задачами, поэтому не можете выполнить данную команду. \
    Вы можете продолжить невыполненное действие, либо отменить его для устранения ошибки.\n*Сбросить текущий процесс?*"
}

LEXICON_COMMANDS: dict = {
    "/all_tasks": "Список всех задач, отсортированный по дате создания 📋\nСтраница {page} / {pages}",
    "/active_tasks": "Список активных задач, отсортированный по дате создания 📋\nСтраница {page} / {pages}",
    "/completed_tasks": "Список выполненных задач, отсортированный по дате создания 📋\nСтраница {page} / {pages}",
    "/create_task": "Выберите категорию для задачи:\nСтраница {page} / {pages}",
    "tasks_from_category": "Страница {page} / {pages}",
}
