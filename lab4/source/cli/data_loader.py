"""Загрузка данных из JSON-файла, лежащего рядом с main.py.

Формат файла:
{
  "list": [ {студент}, ... ],              # список студентов
  "set":  [ {студент}, ... ],              # множество (дубликаты по ключу схлопнутся)
  "dict": { "<student_id>": {студент} },   # словарь id -> студент
  "graph": { "nodes": [id, ...],           # id студентов из "list"
             "edges": [[from_id, to_id, mass], ...] }
}
Студент: {"student_id": int, "name": str, "group": str, "age": int, "gpa": float}
"""
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from source.models.student import Student


class DataFileError(Exception):
    """Файл данных не найден или имеет неверный формат."""


@dataclass
class Dataset:
    students: list[Student] = field(default_factory=list)
    unique_students: set[Student] = field(default_factory=set)
    students_by_id: dict[int, Student] = field(default_factory=dict)
    graph_nodes: list[int] = field(default_factory=list)
    graph_edges: list[tuple[int, int, int]] = field(default_factory=list)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise DataFileError(f"файл данных не найден: {path}") from None
    except OSError as error:
        raise DataFileError(f"не удалось прочитать {path}: {error}") from None
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise DataFileError(f"{path.name}: неверный JSON (строка {error.lineno}): {error.msg}") from None
    if not isinstance(data, dict):
        raise DataFileError(f"{path.name}: на верхнем уровне должен быть объект")
    return data


def _students(raw: Any, section: str) -> list[Student]:
    if not isinstance(raw, list):
        raise DataFileError(f"раздел «{section}» должен быть массивом")
    result = []
    for index, item in enumerate(raw):
        try:
            result.append(Student.from_dict(item))
        except (ValueError, TypeError) as error:
            raise DataFileError(f"раздел «{section}», элемент {index}: {error}") from None
    return result


def load_data(path: Path) -> Dataset:
    data = _read_json(path)
    dataset = Dataset()

    dataset.students = _students(data.get("list", []), "list")
    ids = [s.student_id for s in dataset.students]
    if len(ids) != len(set(ids)):
        raise DataFileError("раздел «list»: повторяются student_id")

    dataset.unique_students = set(_students(data.get("set", []), "set"))

    raw_dict = data.get("dict", {})
    if not isinstance(raw_dict, dict):
        raise DataFileError("раздел «dict» должен быть объектом")
    for key, value in raw_dict.items():
        try:
            student_id = int(key)
        except ValueError:
            raise DataFileError(f"раздел «dict»: ключ «{key}» не целое число") from None
        try:
            student = Student.from_dict(value)
        except (ValueError, TypeError) as error:
            raise DataFileError(f"раздел «dict», ключ {key}: {error}") from None
        if student.student_id != student_id:
            raise DataFileError(f"раздел «dict»: ключ {key} не совпадает с student_id {student.student_id}")
        dataset.students_by_id[student_id] = student

    graph = data.get("graph", {})
    if not isinstance(graph, dict):
        raise DataFileError("раздел «graph» должен быть объектом")
    known = set(ids)
    nodes = graph.get("nodes", [])
    if not isinstance(nodes, list) or not all(isinstance(n, int) for n in nodes):
        raise DataFileError("graph.nodes должен быть массивом целых id")
    for node in nodes:
        if node not in known:
            raise DataFileError(f"graph.nodes: студента с id {node} нет в разделе «list»")
    dataset.graph_nodes = nodes
    for edge in graph.get("edges", []):
        if (not isinstance(edge, list) or len(edge) != 3
                or not all(isinstance(x, int) and not isinstance(x, bool) for x in edge)):
            raise DataFileError(f"graph.edges: ребро {edge} должно быть [from, to, mass] из целых")
        if edge[0] not in nodes or edge[1] not in nodes:
            raise DataFileError(f"graph.edges: ребро {edge} ссылается на вершину не из graph.nodes")
        dataset.graph_edges.append((edge[0], edge[1], edge[2]))
    return dataset
