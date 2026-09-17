from typing import List
from src.matrix.classes.matrix import Matrix

class ZeroMatrix(Matrix):
    def __init__(self, data: List[List[float]]) -> float:
        super().__init__(data)
        if not self.is_zero():
            raise ValueError("Матрица должна быть симметричной")