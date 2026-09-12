import math
from functools import total_ordering
from typing import Iterable

@total_ordering
class Vector:
    @staticmethod
    def cos_between_the_vectors(vec1: "Vector", vec2: "Vector"):
        Vector._check_vector(vec1)
        Vector._check_vector(vec2)
        return (vec1 * vec2) / (vec1.length * vec2.length)
    
    @staticmethod
    def _check_vector(other) -> None:
        if not isinstance(other, Vector):
            raise TypeError("Неправильный тип данных: переданный аргумент не типа Vector")
    
    def __init__(self, 
                 x: float | int = 0.0, 
                 y: float | int = 0.0,
                 z: float | int = 0.0,
                ) -> None:
        """
            Cущность вектора
        Args:
            x (float | int): абсцисса конца вектора
            y (float | int): ордината конца вектора
            z (float | int): апликата конца вектора

            Условимся, что начало вектора: (0, 0 ,0)
        """
        self.x: float | int = x
        self.y: float | int = y
        self.z: float | int = z

    @classmethod
    def generate_from_string(cls, text: str) -> "Vector":
        try:
            x, y, z, *rest = map(float, text.split())
        except ValueError:
            raise ValueError("Некорректный тип данных")
        if len(rest) != 0:
            raise ValueError("Некорректный формат строки: ожидались 3 числа")
        return cls(x, y, z)

    @classmethod
    def generate_from_iterable(cls, data: Iterable[float]) -> "Vector":
        if isinstance(data, str):
            raise TypeError("Ожидается список/кортеж чисел, а не строка")
        if not isinstance(data, Iterable):
            raise TypeError("Неправильный тип данных: передан не Iterable-тип")

        data = list(data)

        if len(data) != 3:
            raise ValueError("Неверное количество аргументов")

        if not all(isinstance(value, (int, float)) for value in data):
            raise TypeError("Неправильный тип данных")

        x, y, z = data
        return cls(x, y, z)
    
    def __copy__(self) -> "Vector":
        return Vector(self.x, self.y, self.z)
    
    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("Неправильный тип данных")
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("Неправильный тип данных")
        self._y = value

    @property
    def z(self) -> float:
        return self._z

    @z.setter
    def z(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("Неправильный тип данных")
        self._z = value

    @property
    def length(self) -> float:
        return math.sqrt(self._x ** 2 + self._y ** 2 + self._z ** 2)

    def __neg__(self) -> "Vector":
        return Vector(-self._x, -self._y, -self._z)

    def __add__(self, other) -> "Vector":
        self._check_vector(other)
        return Vector(self._x + other._x, self._y + other._y, self._z + other._z)

    def __radd__(self, other) -> "Vector":
        if other == 0:
            return self
        return self.__add__(other)

    def __sub__(self, other):
        self._check_vector(other)
        return Vector(self._x - other._x, self._y - other._y, self._z - other._z)

    def __mul__(self, other) -> "float | Vector":
        if isinstance(other, (float, int)):
            return Vector(self._x * other, self._y * other, self._z * other)
        self._check_vector(other)
        return self._x * other._x + self._y * other._y + self._z * other._z

    def __rmul__(self, other) -> "float | Vector":
        return self.__mul__(other)

    def __matmul__(self, other) -> "Vector":
        self._check_vector(other)
        return Vector(self._y * other._z - self._z * other._y,
                      self._z * other._x - self._x * other._z,
                      self._x * other._y - self._y * other._x)

    def __rmatmul__(self, other):
        return -self.__matmul__(other)

    def __truediv__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("Неправильный тип данных")
        if value == 0:
            raise ZeroDivisionError("Нельзя делить на ноль")
        return Vector(self._x / value, self._y / value, self._z / value)

    def __rtruediv__(self, other):
        return NotImplemented

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vector):
            raise TypeError("Неправильный тип данных: переданный аргумент не типа Vector")
        return math.isclose(self.length, other.length)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Vector):
            raise TypeError("Неправильный тип данных: переданный аргумент не типа Vector")
        return self.length < other.length

    __hash__ = None #т.к. объект не иммутабельный запрещаем хэширование нахуй

    
    def __str__(self):
        return f"{self.x} {self.y} {self.z}"    
    
    