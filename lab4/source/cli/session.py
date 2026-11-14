"""Состояние приложения: коллекции студентов и граф."""
from pathlib import Path

from source.cli.data_loader import Dataset, load_data
from source.cli.lab_api import OGraphAdjacencyList
from source.models.student import Student


class Session:
    def __init__(self, data_path: Path) -> None:
        self.data_path = data_path
        self.students: list[Student] = []
        self.unique_students: set[Student] = set()
        self.students_by_id: dict[int, Student] = {}
        self.graph: OGraphAdjacencyList = OGraphAdjacencyList()
        self.load()

    def load(self) -> None:
        """Читает файл заново: все коллекции и граф возвращаются к состоянию из файла."""
        dataset: Dataset = load_data(self.data_path)
        self.students = dataset.students
        self.unique_students = dataset.unique_students
        self.students_by_id = dataset.students_by_id
        self.graph = OGraphAdjacencyList()
        by_id = {s.student_id: s for s in dataset.students}
        for node_id in dataset.graph_nodes:
            self.graph.create_node(by_id[node_id])
        for source, target, mass in dataset.graph_edges:
            self.graph.create_edge(by_id[source], by_id[target], mass)

    # ---- поиск и изменение ----
    def find(self, student_id: int) -> Student | None:
        for student in self.students:
            if student.student_id == student_id:
                return student
        return self.students_by_id.get(student_id)

    def add_student(self, student: Student) -> None:
        if self.find(student.student_id) is not None:
            raise ValueError(f"студент с id {student.student_id} уже есть")
        self.students.append(student)
        self.unique_students.add(student)
        self.students_by_id[student.student_id] = student

    def remove_student(self, student_id: int) -> Student:
        student = self.find(student_id)
        if student is None:
            raise ValueError(f"студента с id {student_id} нет")
        self.students = [s for s in self.students if s.student_id != student_id]
        self.unique_students = {s for s in self.unique_students if s.student_id != student_id}
        self.students_by_id.pop(student_id, None)
        if self.graph.has_node(student):
            self.graph.delete_node(student)
        return student
