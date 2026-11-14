"""Консольное приложение лабы 4: Student, сортировки и граф."""
from pathlib import Path

from source.cli import graph_menu, sort_menu, student_menu
from source.cli.console import report_errors, run_menu
from source.cli.data_loader import DataFileError
from source.cli.session import Session


def _reload(session: Session) -> None:
    session.load()
    print(f"  Данные перезагружены из {session.data_path.name}.")


def run(data_path: Path) -> None:
    try:
        session = Session(data_path)
    except DataFileError as error:
        print(f"Не удалось загрузить данные: {error}")
        return
    print(f"Данные загружены из {data_path.name}: студентов в списке {len(session.students)}, "
          f"в множестве {len(session.unique_students)}, в словаре {len(session.students_by_id)}, "
          f"в графе {session.graph.nodes_count} вершин и {session.graph.edges_count} рёбер.")

    try:
        run_menu("Лабораторная 4: сортировки и граф", {
            "1": ("Студенты (коллекции, сравнение, контракты)", lambda: student_menu.run(session)),
            "2": ("Сортировать коллекцию", lambda: sort_menu.sort_collection(session)),
            "3": ("Показать устойчивость сортировок", lambda: sort_menu.compare_stability(session)),
            "4": ("Граф", lambda: graph_menu.run(session)),
            "5": ("Перезагрузить данные из файла", lambda: _reload_with_errors(session)),
        }, back="Выход")
    except (EOFError, KeyboardInterrupt):
        print("\nЗавершение работы.")
        return
    print("Завершение работы.")


def _reload_with_errors(session: Session) -> None:
    try:
        _reload(session)
    except DataFileError as error:
        print(f"  Не удалось перезагрузить: {error}")
