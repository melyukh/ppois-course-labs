"""Мелкие помощники для ввода и вывода в консоли."""
from typing import Callable, Optional

from source.cli.lab_api import HANDLED_ERRORS

MenuEntries = dict[str, tuple[str, Callable[[], None]]]


def ask(prompt: str) -> str:
    return input(prompt).strip()


def ask_int(prompt: str, minimum: Optional[int] = None, maximum: Optional[int] = None) -> int:
    while True:
        raw = ask(prompt)
        try:
            value = int(raw)
        except ValueError:
            print("  Нужно целое число.")
            continue
        if (minimum is not None and value < minimum) or (maximum is not None and value > maximum):
            print(f"  Допустимый диапазон: {minimum}..{maximum}.")
            continue
        return value


def ask_float(prompt: str) -> float:
    while True:
        raw = ask(prompt).replace(",", ".")
        try:
            return float(raw)
        except ValueError:
            print("  Нужно число.")


def ask_yes_no(prompt: str, default: bool = False) -> bool:
    suffix = " [Д/н]: " if default else " [д/Н]: "
    while True:
        raw = ask(prompt + suffix).lower()
        if not raw:
            return default
        if raw in ("д", "да", "y", "yes"):
            return True
        if raw in ("н", "нет", "n", "no"):
            return False
        print("  Ответьте «д» или «н».")


def choose(title: str, labels: list[str], back: str = "Назад") -> Optional[int]:
    """Показывает пронумерованный список, возвращает индекс (с нуля) или None для «Назад»."""
    print(f"\n{title}")
    for number, label in enumerate(labels, start=1):
        print(f"  {number}. {label}")
    print(f"  0. {back}")
    choice = ask_int("Выбор: ", 0, len(labels))
    return None if choice == 0 else choice - 1


def report_errors(action: Callable[[], None]) -> None:
    """Вызывает действие меню; ошибки лабы печатает сообщением, а не падает."""
    try:
        action()
    except HANDLED_ERRORS as error:
        print(f"\n  Ошибка ({type(error).__name__}): {error}")


def run_menu(title: str, entries: MenuEntries, back: str = "Назад") -> None:
    while True:
        print(f"\n=== {title} ===")
        for key, (label, _) in entries.items():
            print(f"{key}. {label}")
        print(f"0. {back}")
        choice = ask("Выбор: ")
        if choice == "0":
            return
        entry = entries.get(choice)
        if entry is None:
            print("Неверный выбор, попробуйте снова")
            continue
        report_errors(entry[1])


def print_students(students, title: str = "") -> None:
    if title:
        print(f"\n{title}")
    print(f"{'id':>5}  {'имя':<22}  {'группа':<7}  {'воз':>3}  {'балл':>5}")
    print("-" * 50)
    count = 0
    for student in students:
        print(student.row())
        count += 1
    if count == 0:
        print("(пусто)")


def print_items(items, title: str = "") -> None:
    """Печатает студентов таблицей, остальные элементы (числа и т. п.) в строку."""
    items = list(items)
    if items and all(hasattr(item, "row") for item in items):
        print_students(items, title)
    else:
        if title:
            print(f"\n{title}")
        print(items if items else "(пусто)")
