import calendar
import datetime

from enum import Enum
from typing import Tuple, Any, Optional, Dict


class CategoryColors(Enum):
    RED = "#F44336"  # Красный
    GREEN = "#4CAF50"  # Зеленый
    BLUE = "#2196F3"  # Синий
    YELLOW = "#FFC107"  # Желтый
    ORANGE = "#FF9800"  # Оранжевый
    PURPLE = "#9C27B0"  # Фиолетовый
    PINK = "#E91E63"  # Розовый
    BROWN = "#795548"  # Коричневый
    GREY = "#9E9E9E"  # Серый
    BLACK = "#212121"  # Черный
    WHITE = "#FFFFFF"  # Белый
    CYAN = "#00BCD4"  # Голубой
    LIME = "#C0CA33"  # Лаймовый
    TEAL = "#009688"  # Зелено-голубой
    INDIGO = "#3F51B5"  # Индиго
    DEEP_PURPLE = "#673AB7"  # Темно-фиолетовый
    LIGHT_BLUE = "#03A9F4"  # Светло-голубой
    LIGHT_GREEN = "#8BC34A"  # Светло-зеленый
    LIGHT_GREY = "#EEEEEE"  # Светло-серый
    AMBER = "#FFC107"  # Янтарный
    DEEP_ORANGE = "#FF5722"  # Темно-оранжевый
    LIGHT_PINK = "#F48FB1"  # Светло-розовый


priority_converter = {
    "low": 3,
    "medium": 2,
    "high": 1
}

inverse_priority_converter = {
    3: "Низкий",
    2: "Средний",
    1: "Высокий"
}


def format_date(date_string: str) -> str:
    """
    Преобразует дату из формата 'гггг-м-д' в формат 'гггг-мм-дд'.

    Args:
        date_string: Строка с датой в формате 'гггг-м-д'.

    Returns:
        Строка с датой в формате 'гггг-мм-дд' или None, если формат ввода неверный.
    """

    date_object = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    formatted_date = date_object.strftime('%Y-%m-%d')

    return formatted_date


def set_edited_task_data(task: Dict, edited_param: str, edited_data: Any) -> Dict:
    data = {
        "name": task["name"],
        "description": task["description"],
        "priority": task["priority"],
        "category_id": task["category_id"],
        "date": task["date"]
    }
    data[edited_param] = edited_data

    return data


def get_month_by_number(month: int) -> str:
    return calendar.month_name[month]


def get_day_by_number(day: int) -> str:
    return calendar.day_name[day]


def get_month_data(year: int, month: int) -> Tuple[int, int]:
    return calendar.monthrange(year, month)


if __name__ == "__main__":
    date = datetime.date.today()
    year, month, day = date.year, date.month, date.day
    for day in range(7):
        print(calendar.day_name[day])
    print()
    for month in range(1, 13):
        print(calendar.monthrange(year, month))
