"""Меню «Граф»: операции над ориентированным графом студентов и его итераторы."""
from source.cli.console import ask_int, choose, print_students, run_menu
from source.cli.session import Session
from source.models.student import Student


def _student(session: Session, prompt: str) -> Student:
    student_id = ask_int(prompt)
    student = session.find(student_id)
    if student is None:
        raise ValueError(f"студента с id {student_id} нет ни в одной коллекции; создайте его в меню «Студенты»")
    return student


def _show_nodes(session: Session) -> None:
    graph = session.graph
    print_students(graph.nodes(), f"Вершины (прямой порядок), всего {graph.nodes_count}:")
    print_students(reversed(graph), "Вершины (обратный порядок, reversed):")


def _show_edges(session: Session) -> None:
    graph = session.graph
    print(f"\nРёбра, всего {graph.edges_count}:")
    for source, target in graph.edges():
        print(f"  {source}  ->  {target}   вес {graph.edge_mass(source, target)}")


def _add_node(session: Session) -> None:
    student = _student(session, "id студента, которого добавить как вершину: ")
    session.graph.create_node(student)
    print(f"  Вершина добавлена: {student}")


def _delete_node(session: Session) -> None:
    student = _student(session, "id вершины для удаления: ")
    session.graph.delete_node(student)
    print(f"  Вершина удалена вместе со всеми её рёбрами (входящими и исходящими): {student}")


def _add_edge(session: Session) -> None:
    source = _student(session, "id начала ребра: ")
    target = _student(session, "id конца ребра: ")
    mass = ask_int("Вес ребра (целое): ")
    session.graph.create_edge(source, target, mass)
    print(f"  Ребро {source} -> {target} (вес {mass}) добавлено; если оно уже было, вес перезаписан.")


def _delete_edge(session: Session) -> None:
    source = _student(session, "id начала ребра: ")
    target = _student(session, "id конца ребра: ")
    session.graph.delete_edge(source, target)
    print("  Ребро удалено.")


def _has_node(session: Session) -> None:
    student = _student(session, "id студента: ")
    print(f"  В графе: {session.graph.has_node(student)}")


def _has_edge(session: Session) -> None:
    source = _student(session, "id начала: ")
    target = _student(session, "id конца: ")
    print(f"  Ребро {source} -> {target}: {session.graph.has_edge(e_from=source, e_to=target)}")


def _node_power(session: Session) -> None:
    student = _student(session, "id вершины: ")
    power = session.graph.node_power(student)
    print(f"  Входящих рёбер: {power['from']}, исходящих: {power['to']}")


def _edge_mass(session: Session) -> None:
    source = _student(session, "id начала: ")
    target = _student(session, "id конца: ")
    print(f"  Вес ребра {source} -> {target}: {session.graph.edge_mass(source, target)}")


def _incident(session: Session) -> None:
    student = _student(session, "id вершины: ")
    edges = list(session.graph.incident_edges(student))
    print(f"\nИсходящие рёбра вершины {student} ({len(edges)}):")
    for source, target in edges:
        print(f"  {source}  ->  {target}   вес {session.graph.edge_mass(source, target)}")


def _adjacent(session: Session) -> None:
    student = _student(session, "id вершины: ")
    print_students(session.graph.adjacent_nodes(student), f"Вершины, в которые ведёт ребро из {student}:")


def _walk(iterator, title: str) -> None:
    """Ручной обход двунаправленным итератором: n — вперёд, p — назад, q — выход."""
    print(f"\n{title}\n  n — next, p — prev, q — выход")
    while True:
        command = input("  > ").strip().lower()
        if command in ("q", ""):
            return
        try:
            if command == "n":
                print("  next ->", next(iterator))
            elif command == "p":
                print("  prev ->", iterator.prev())
            else:
                print("  Команды: n, p, q")
        except StopIteration:
            print("  (граница: элементов больше нет в эту сторону)")
        except RuntimeError as error:
            print(f"  RuntimeError: {error}")
            return


def _walk_menu(session: Session) -> None:
    graph = session.graph
    options = ["Вершины", "Вершины в обратном порядке", "Рёбра", "Исходящие рёбра вершины", "Смежные вершины вершины"]
    choice = choose("По чему ходить итератором?", options)
    if choice is None:
        return
    if choice == 0:
        _walk(graph.nodes(), "Итератор вершин")
    elif choice == 1:
        _walk(reversed(graph), "Обратный итератор вершин")
    elif choice == 2:
        _walk(graph.edges(), "Итератор рёбер (пары from, to)")
    elif choice == 3:
        _walk(graph.incident_edges(_student(session, "id вершины: ")), "Итератор исходящих рёбер вершины")
    else:
        _walk(graph.adjacent_nodes(_student(session, "id вершины: ")), "Итератор смежных вершин")


def _invalidation_demo(session: Session) -> None:
    graph = session.graph
    if graph.nodes_count < 2:
        raise ValueError("для демонстрации нужно хотя бы две вершины")
    temp = Student("Временный", -1, "—", 18, 0.0)
    iterator = graph.nodes()
    print(f"\n  1) Создали итератор вершин и взяли первую: {next(iterator)}")
    graph.create_node(temp)
    print(f"  2) Изменили граф во время итерации (добавили вершину {temp})")
    try:
        next(iterator)
        print("  3) итератор продолжил работу (инвалидации нет)")
    except RuntimeError as error:
        print(f"  3) next() -> RuntimeError: {error}")
    finally:
        graph.delete_node(temp)
        print("  4) временная вершина удалена; новый итератор работает как обычно")


def _reload_graph(session: Session) -> None:
    session.load()
    print("  Все данные и граф перезагружены из файла.")


def run(session: Session) -> None:
    run_menu("Граф (ориентированный, список смежности)", {
        "1": ("Показать вершины (прямо и reversed)", lambda: _show_nodes(session)),
        "2": ("Показать рёбра с весами", lambda: _show_edges(session)),
        "3": ("Добавить вершину (студента по id)", lambda: _add_node(session)),
        "4": ("Удалить вершину", lambda: _delete_node(session)),
        "5": ("Добавить ребро", lambda: _add_edge(session)),
        "6": ("Удалить ребро", lambda: _delete_edge(session)),
        "7": ("Есть ли вершина", lambda: _has_node(session)),
        "8": ("Есть ли ребро", lambda: _has_edge(session)),
        "9": ("Степень вершины (входящие и исходящие)", lambda: _node_power(session)),
        "10": ("Вес ребра", lambda: _edge_mass(session)),
        "11": ("Исходящие рёбра вершины", lambda: _incident(session)),
        "12": ("Смежные вершины", lambda: _adjacent(session)),
        "13": ("Походить итератором вперёд и назад", lambda: _walk_menu(session)),
        "14": ("Демонстрация: изменение графа ломает итератор", lambda: _invalidation_demo(session)),
        "15": ("Вернуть граф к состоянию из файла", lambda: _reload_graph(session)),
    })
