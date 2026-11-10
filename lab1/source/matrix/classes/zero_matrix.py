from typing import List
from source.matrix.classes.matrix import Matrix

class ZeroMatrix(Matrix):
    def __init__(self, data: List[List[float]]) -> None:
        super().__init__(data)
        if not self.is_zero():
            raise ValueError("Матрица должна быть нулевой")