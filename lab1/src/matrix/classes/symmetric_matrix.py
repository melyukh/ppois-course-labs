from typing import List
from src.matrix.classes.square_matrix import SquareMatrix

class SymmetricMatrix(SquareMatrix):
    def __init__(self, data: List[List[float]]) -> float:
        super().__init__(data)
        if not self.is_symmetric():
            raise ValueError("Матрица должна быть симметричной")