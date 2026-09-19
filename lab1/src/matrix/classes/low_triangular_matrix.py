from typing import List
from src.matrix.classes.matrix import Matrix
from src.matrix.classes.square_matrix import SquareMatrix

class LowTriangularMatrix(SquareMatrix):
    def __init__(self, data: List[List[float]]) -> None:
        super().__init__(data)
        if not self.is_low_triangular():
            raise ValueError("Матрица должна быть нижнетреугольной")