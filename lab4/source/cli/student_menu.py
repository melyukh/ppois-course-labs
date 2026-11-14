"""Меню «Студенты»: коллекции, добавление/удаление, сравнение, проверка контрактов."""
from collections.abc import Hashable

from source.cli.console import (ask, ask_float, ask_int, choose, print_students, run_menu)
from source.cli.session import Session
from source.models.student import Student


def _show_collections(session: Session) -> None:
    print_students(session.students, f"Список (list), {len(session.students)} шт.")
    print_students(sorted(session.unique_students), f"Множество (set), {len(session.unique_students)} шт., по возрастанию для читаемости")
    print_students(session.students_by_id.values(), f"Словарь (dict id -> студент), {len(session.students_by_id)} шт.")


def _read_student(session: Session) -> Student:
    student_id = ask_int("id студента: ")
    if session.find(student_id) is not None:
        raise ValueError(f"студент с id {student_id} уже есть")
    name = ask("Имя: ")
    group = ask("Группа: ")
    age = ask_int("Возраст: ", 0, 120)
    gpa = ask_float("Средний балл (0..10): ")
    return Student(name=name, student_id=student_id, group=group, age=age, gpa=gpa)


def _add_student(session: Session) -> None:
    student = _read_student(session)
    session.add_student(student)
    print(f"  Добавлен: {student!r}")
    print("  Он лежит в списке, множестве и словаре; в граф его можно добавить из меню графа.")


def _remove_student(session: Session) -> None:
    student = session.remove_student(ask_int("id студента для удаления: "))
    print(f"  Удалён из всех коллекций и графа: {student}")


def _pick_two(session: Session) -> tuple[Student, Student]:
    first = session.find(ask_int("id первого студента: "))
    second = session.find(ask_int("id второго студента: "))
    if first is None or second is None:
        raise ValueError("студент с таким id не найден")
    return first, second


def _compare(session: Session) -> None:
    a, b = _pick_two(session)
    print(f"\n  a = {a!r}\n  b = {b!r}")
    print(f"  a == b : {a == b}")
    print(f"  a <  b : {a < b}")
    print(f"  a >  b : {a > b}")
    print(f"  hash(a) == hash(b) : {hash(a) == hash(b)}")
    print("  Сравниваются только ключевые поля (имя, id), остальные поля данные.")


def _contracts(session: Session) -> None:
    sample = session.students[0] if session.students else Student("Пример", 0)
    print(f"\n  Проверяем на {sample.name}:")
    print(f"  isinstance(x, Hashable)      : {isinstance(sample, Hashable)}")
    for method in ("__eq__", "__hash__", "__lt__", "__le__", "__gt__", "__ge__"):
        print(f"  есть {method:<8}              : {hasattr(sample, method)}")
    print("  Попытка изменить ключевое поле:")
    try:
        sample.name = "другое"          # type: ignore[misc]
    except AttributeError as error:
        print(f"    запрещено ({error}): иначе хеш в set/dict/графе стал бы неверным")
    print("  Данные (group, age, gpa) менять можно, на хеш они не влияют.")
    twin = Student(sample.name, sample.student_id, group="другая", age=99, gpa=1.0)
    print(f"  Двойник с тем же ключом и другими данными: равен={twin == sample}, "
          f"hash равен={hash(twin) == hash(sample)}, в set схлопывается={len({sample, twin}) == 1}")


def _dedup_demo(session: Session) -> None:
    raw = list(session.students) + list(session.unique_students)
    print(f"\n  Всего записей (список + множество): {len(raw)}")
    print(f"  После превращения в set: {len(set(raw))} уникальных (по ключу имя+id)")


def run(session: Session) -> None:
    run_menu("Студенты", {
        "1": ("Показать списки, множество и словарь", lambda: _show_collections(session)),
        "2": ("Добавить студента", lambda: _add_student(session)),
        "3": ("Удалить студента по id", lambda: _remove_student(session)),
        "4": ("Сравнить двух студентов (==, <, hash)", lambda: _compare(session)),
        "5": ("Проверить контракты Hashable / Comparable", lambda: _contracts(session)),
        "6": ("Демонстрация: дубликаты схлопываются в set", lambda: _dedup_demo(session)),
    })
