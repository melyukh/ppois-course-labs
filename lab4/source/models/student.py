from __future__ import annotations

from functools import total_ordering
from typing import Any

from source.exceptions.badTypeException import BadTypeError


@total_ordering
class Student:
    """Демонстрационный тип для сортировок и графа.

    Контракты:
      Hashable   — __hash__ и __eq__ по ключу (name, student_id); ключ неизменяем.
      Comparable — __lt__ по тому же ключу (остальное достраивает total_ordering),
                   порядок согласован с равенством: a == b  <=>  не a < b и не b < a.
    Остальные поля (group, age, gpa) — просто данные: в сравнение и хеш не входят,
    поэтому два студента с одинаковым ключом считаются одним и тем же элементом.
    """

    __slots__ = ("_name", "_student_id", "group", "age", "gpa")

    def __init__(self, name: str, student_id: int, group: str = "", age: int = 18, gpa: float = 0.0) -> None:
        if not isinstance(name, str):
            raise BadTypeError(f"name должен быть str, получен {type(name).__name__}")
        if isinstance(student_id, bool) or not isinstance(student_id, int):
            raise BadTypeError(f"student_id должен быть int, получен {type(student_id).__name__}")
        if not isinstance(group, str):
            raise BadTypeError(f"group должен быть str, получен {type(group).__name__}")
        if isinstance(age, bool) or not isinstance(age, int):
            raise BadTypeError(f"age должен быть int, получен {type(age).__name__}")
        if isinstance(gpa, bool) or not isinstance(gpa, (int, float)):
            raise BadTypeError(f"gpa должен быть числом, получен {type(gpa).__name__}")
        if not name.strip():
            raise ValueError("name не должен быть пустым")
        if not 0 <= age <= 120:
            raise ValueError("age должен быть в диапазоне 0..120")
        if not 0 <= gpa <= 10:
            raise ValueError("gpa должен быть в диапазоне 0..10")

        self._name = name.strip()
        self._student_id = student_id
        self.group = group.strip()
        self.age = age
        self.gpa = float(gpa)

    # ---- ключевые поля (только чтение: иначе сломается хеш в set/dict/графе) ----
    @property
    def name(self) -> str:
        return self._name

    @property
    def student_id(self) -> int:
        return self._student_id

    def _key(self) -> tuple[str, int]:
        return (self._name, self._student_id)

    # ---- Hashable ----
    def __hash__(self) -> int:
        return hash(self._key())

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self._key() == other._key()

    # ---- Comparable ----
    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self._key() < other._key()

    # ---- представление ----
    def __str__(self) -> str:
        return f"{self._student_id} {self._name}"

    def __repr__(self) -> str:
        return (f"Student(name={self._name!r}, student_id={self._student_id}, "
                f"group={self.group!r}, age={self.age}, gpa={self.gpa})")

    def row(self) -> str:
        return f"{self._student_id:>5}  {self._name:<22}  {self.group:<7}  {self.age:>3}  {self.gpa:>5.2f}"

    # ---- сериализация ----
    def to_dict(self) -> dict[str, Any]:
        return {"student_id": self._student_id, "name": self._name,
                "group": self.group, "age": self.age, "gpa": self.gpa}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Student":
        if not isinstance(data, dict):
            raise ValueError(f"студент должен быть объектом JSON, получено {type(data).__name__}")
        missing = [f for f in ("name", "student_id") if f not in data]
        if missing:
            raise ValueError(f"у студента нет обязательных полей: {', '.join(missing)}")
        return cls(
            name=data["name"],
            student_id=data["student_id"],
            group=data.get("group", ""),
            age=data.get("age", 18),
            gpa=data.get("gpa", 0.0),
        )
