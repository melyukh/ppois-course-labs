from typing import List
from math import sqrt
from src.matrix.classes.base_matrix import BaseMatrix

class Matrix(BaseMatrix):
    def __init__(self, data: List[List[int]]) -> None:
        if not data or not data[0]:
            raise ValueError("Матрица не может быть пустой")
        for i in range(1, len(data)):
            if len(data[i]) != len(data[0]):
                raise ValueError("Неравная длина строк")
        super().__init__(data)

    def _build(self, data: List[List[int]]) -> "BaseMatrix":
        return Matrix.create(data)

    @classmethod
    def generate_from_string(cls, line: str) -> "BaseMatrix":
        result = []
        data = [row for row in line.split('\n') if row]
        if not data or not data[0]:
            raise ValueError("Матрица не может быть пустой")
        try:
            row = list(map(float, data[0].split()))
            result.append(row)
            for i in range(1, len(data)):
                next_row = list(map(float, data[i].split()))
                if len(row) != len(next_row):
                    raise ValueError("Неравная длина строк")
                result.append(next_row)
        except ValueError:
            raise ValueError("Неверный тип данных")

        return Matrix.create(result)

    @classmethod
    def generate_from_file(cls, path: str) -> "BaseMatrix":
        with open(path, "r") as f:
            lines = f.readlines()
    
        data = [[float(x) for x in line.split()] for line in lines if line.strip()]
    
        if not data or not all(len(row) == len(data[0]) for row in data):
            raise ValueError("Некорректный формат файла: строки разной длины")
    
        return Matrix.create(data)

    @staticmethod
    def create(data: List[List[int]]) -> "BaseMatrix":
        from src.matrix.classes.identity_matrix import IdentityMatrix
        from src.matrix.classes.diagonal_matrix import DiagonalMatrix
        from src.matrix.classes.symmetric_matrix import SymmetricMatrix
        from src.matrix.classes.square_matrix import SquareMatrix
        from src.matrix.classes.zero_matrix import ZeroMatrix

        temp = Matrix(data)

        if temp.is_identity():
            return IdentityMatrix(data)
        elif temp.is_diagonal():
            return DiagonalMatrix(data)
        elif temp.is_symmetric():
            return SymmetricMatrix(data)
        elif temp.is_high_triangular():
            return HighTriangularMatrix(data)
        elif temp.is_low_triangular():
            return LowTriangularMatrix(data)
        elif temp.is_square():
            return SquareMatrix(data)
        elif temp.is_zero():
            return ZeroMatrix(data)
        return Matrix(data)


    def __add__(self, other) -> "BaseMatrix":
        if Matrix._is_matrix(other):
            if self.rows != other.rows or self.columns != other.columns:
                raise ValueError("Несоразмерные матрицы\n")
            new_data = [[self.matrix[i][j] + other.matrix[i][j] for j in range(self.columns)] for i in range(self.rows)]
            return Matrix.create(new_data)
        elif Matrix._is_num(other):
            new_data = [[self.matrix[i][j] + other for j in range(self.columns)] for i in range(self.rows)]
            return Matrix.create(new_data)
        else:
            raise TypeError("Невозможно сложить матрицу с переданным типом данных\n")

    def __radd__(self, other) -> "BaseMatrix":
        return self.__add__(other)


    def __sub__(self, other) -> "BaseMatrix":
        if Matrix._is_matrix(other):
            if self.rows != other.rows or self.columns != other.columns:
                raise ValueError("Несоразмерные матрицы\n")
            new_data = [[self.matrix[i][j] - other.matrix[i][j] for j in range(self.columns)] for i in range(self.rows)]
            return Matrix.create(new_data)
        elif Matrix._is_num(other):
            new_data = [[self.matrix[i][j] - other for j in range(self.columns)] for i in range(self.rows)]
            return Matrix.create(new_data)
        else:
            raise TypeError("Невозможно отнять от матрицы переданный тип данных\n")

    def __rsub__(self, other):
        return NotImplemented


    def __mul__(self, other):
        if Matrix._is_matrix(other):
            if self.columns != other.rows:
                raise ValueError("Несоразмерные матрицы\n")
            result = [[0.0] * other.columns for _ in range(self.rows)]
            for i in range(self.rows):
                for j in range(other.columns):
                    for k in range(self.columns):
                        result[i][j] += self._data[i][k] * other._data[k][j]
            return Matrix.create(result)
        elif Matrix._is_num(other):
            new_data = [[self.matrix[i][j] * other for j in range(self.columns)] for i in range(self.rows)]
            return Matrix.create(new_data)
        else:
            raise TypeError("Невозможно перемножить матрицу с переданным типом данных\n")

    def __rmul__(self, other):
        return self.__mul__(other)


    def __truediv__(self, other):
        if Matrix._is_num(other):
            new_data = [[self.matrix[i][j] / other for j in range(self.columns)] for i in range(self.rows)]
            return Matrix.create(new_data)
        raise TypeError("Нельзя разделить матрицу на переданный тип данных\n")

    def __rtruediv__(self, other):
        return NotImplemented

    def __str__(self) -> str:
        return '\n'.join([' '.join(map(str, self.matrix[i])) for i in range(self.rows)])

    def norm(self) -> float:
        sum = 0.0
        for i in range(self.rows):
            for j in range(self.columns):
                sum += self.matrix[i][j] * self.matrix[i][j]
        return sqrt(sum)