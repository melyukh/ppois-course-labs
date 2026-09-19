from typing import List
from src.matrix.classes.square_matrix import SquareMatrix
from src.matrix.classes.matrix import Matrix
from functools import reduce

class DiagonalMatrix(SquareMatrix):
    def __init__(self, data: List[List[float]]) -> float:
        super().__init__(data)
        if not self.is_diagonal():
            raise ValueError("Матрица должна быть диагональной")

    def determinant(self):
        return reduce(lambda a, b: a * b, [self.matrix[i][i] for i in range(self.rows)], 1)

    def __mul__(self, other):
        if Matrix._is_matrix(other):
            if self.columns != other.rows:
                raise ValueError("Несоразмерные матрицы\n")
            if not other.is_diagonal():
                return super().__mul__(other)
            result = [[0.0 for _ in range(other.rows)] for _ in range(self.columns)]
            for i in range(self.columns):
                result[i][i] = self.matrix[i][i] * other.matrix[i][i]
            return Matrix.create(result)
        elif Matrix._is_num(other):
            new_data = [[self.matrix[i][j] * other for j in range(self.columns)] for i in range(self.rows)]
            return Matrix.create(new_data)
        else:
            raise TypeError("Невозможно перемножить матрицу с переданным типом данных\n")

    def __pow__(self, number):
        if number < 0: 
            raise ValueError("степень не может быть ниже 0\n")
        if number == 0:
            data = [[1 if i == j else 0 for j in range(self.rows)] for i in range(self.rows)]
            return Matrix.create(data)
        if number == 1:
            return Matrix.create(self.matrix)
        result = [[0.0] * self.columns for _ in range(self.rows)]
        for i in range(self.rows):
            result[i][i] = self.matrix[i][i] ** number
        return Matrix.create(result)
        