"""Меню «Сортировки»: выбор коллекции, алгоритма, ключа, режима."""
from typing import Any, Callable, Optional

from source.cli.console import ask_yes_no, choose, print_items
from source.cli.lab_api import (counting_sort, counting_sort_inplace, insertion_sort,
                                insertion_sort_inplace, selection_sort, selection_sort_inplace)
from source.cli.session import Session

KeyFunc = Optional[Callable[[Any], Any]]

ALGORITHMS = [
    ("Сортировка выбором (selection)", selection_sort, selection_sort_inplace),
    ("Сортировка вставками (insertion)", insertion_sort, insertion_sort_inplace),
    ("Сортировка подсчётом (counting, только целые ключи)", counting_sort, counting_sort_inplace),
]

STUDENT_KEYS: list[tuple[str, KeyFunc]] = [
    ("по умолчанию (порядок класса: имя, id)", None),
    ("id", lambda s: s.student_id),
    ("возраст", lambda s: s.age),
    ("средний балл (дробный, для counting вызовет ошибку)", lambda s: s.gpa),
    ("средний балл * 10, округлённый (целый)", lambda s: round(s.gpa * 10)),
    ("группа (строка, для counting вызовет ошибку)", lambda s: s.group),
    ("длина имени", lambda s: len(s.name)),
]

INT_KEYS: list[tuple[str, KeyFunc]] = [
    ("по умолчанию", None),
    ("остаток от деления на 10", lambda x: x % 10),
    ("по модулю", abs),
]

SOURCES = [
    "Список студентов",
    "Множество студентов",
    "Словарь: значения (студенты)",
    "Словарь: ключи (id, целые числа)",
]


def _items_for(session: Session, source: int) -> list[Any]:
    if source == 0:
        return session.students
    if source == 1:
        return list(session.unique_students)       # порядок множества не определён: сортировка его наведёт
    if source == 2:
        return list(session.students_by_id.values())
    return list(session.students_by_id.keys())


def sort_collection(session: Session) -> None:
    source = choose("Какую коллекцию сортировать?", SOURCES)
    if source is None:
        return
    algorithm = choose("Алгоритм:", [a[0] for a in ALGORITHMS])
    if algorithm is None:
        return
    keys = INT_KEYS if source == 3 else STUDENT_KEYS
    key_index = choose("Ключ сортировки:", [k[0] for k in keys])
    if key_index is None:
        return
    key = keys[key_index][1]
    reverse = ask_yes_no("По убыванию (reversed_sort)?")

    _, copying, inplace = ALGORITHMS[algorithm]
    items = _items_for(session, source)
    print_items(items, "До сортировки:")

    in_place_possible = source == 0
    if in_place_possible and ask_yes_no("Сортировать на месте (список в состоянии приложения изменится)?"):
        inplace(items, key=key, reversed_sort=reverse)
        print_items(items, "После сортировки на месте (изменён сам список):")
        print("  Чтобы вернуть исходный порядок, перезагрузите данные из файла (пункт 4 главного меню).")
        return

    result = copying(items, key=key, reversed_sort=reverse)
    print_items(result, "Результат (новый список, исходная коллекция не изменена):")


def compare_stability(session: Session) -> None:
    """Показывает устойчивость: сортируем по группе, студенты одной группы должны остаться в порядке списка."""
    items = list(session.students)
    key = lambda s: s.group              # noqa: E731  (в каждой группе несколько студентов, ключи равны)
    print_items(items, "Исходный список:")
    for title, copying, _ in ALGORITHMS[:2]:
        print_items(copying(items, key=key), f"{title}, ключ = группа:")
    print("\n  У устойчивой сортировки внутри одной группы студенты идут в том же порядке, что и в исходном списке.")
    print("  Счётная сортировка здесь не участвует: ключ-строка ей не подходит.")
