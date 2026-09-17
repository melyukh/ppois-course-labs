from typing import List
from src.matrix.classes.diagonal_matrix import DiagonalMatrix
from src.matrix.classes.matrix import Matrix

class IdentityMatrix(DiagonalMatrix):
    def __init__(self, data: List[List[float]]) -> float:
        super().__init__(data)
        if not self.is_identity():
            raise ValueError("Матрица должна быть единичной")

    def determinant(self) -> float:
        return 1.0

    def __pow__(self, number: int):
        return Matrix.create(self.matrix)

    def __mul__(self, other):
        if Matrix._is_matrix(other):
            if self.columns != other.rows:
                raise ValueError("Несоразмерные матрицы\n")
            return Matrix.create(other.matrix)
        elif Matrix._is_num(other):
            new_data = [[self.matrix[i][j] * other for j in range(self.columns)] for i in range(self.rows)]
            return Matrix.create(new_data)
        else:
            raise TypeError("Невозможно перемножить матрицу с переданным типом данных\n")