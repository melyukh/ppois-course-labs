from typing import List
from source.matrix.classes.matrix import Matrix
from source.matrix.classes.square_matrix import SquareMatrix

class HighTriangularMatrix(SquareMatrix):
    def __init__(self, data: List[List[float]]) -> None:
        super().__init__(data)
        if not self.is_high_triangular():
            raise ValueError("Матрица должна быть верхнетреугольной")