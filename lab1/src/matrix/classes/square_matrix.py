from typing import List
from src.matrix.classes.matrix import Matrix
from functools import reduce

class SquareMatrix(Matrix):
    def __init__(self, data: List[List[float]]) -> None:
        super().__init__(data)
        if not self.is_square():
            raise ValueError("Матрица должна быть квадратной")


    def determinant(self) -> float:
        swap_count = 0
        temp = [row[:] for row in self.matrix]
        length = len(temp[0])

        for i in range(length):
            if temp[i][i] == 0:
                has_not_zero = False
                for j in range(i + 1, length):
                    if temp[j][i] != 0:
                        has_not_zero = True
                        swap_count += 1
                        temp[i], temp[j] = temp[j], temp[i]
                        break
                if not has_not_zero:
                    return 0.0
            for j in range(i + 1, length):
                factor = temp[j][i] / temp[i][i]
                temp[j] = [temp[j][k] - factor * temp[i][k] for k in range(length)]

        return (-1) ** swap_count * reduce(lambda a, b: a * b, [temp[i][i] for i in range(length)], 1)

    def __pow__(self, number: int):
        if number < 0: 
            raise ValueError("степень не может быть ниже 0\n")
        if number == 0:
            data = [[1 if i == j else 0 for j in range(self.rows)] for i in range(self.rows)]
            return Matrix.create(data)
        if number == 1:
            return Matrix.create(self.matrix)

        if number % 2 == 0:
            val = self ** (number // 2)
            return val * val
        return self * self ** (number - 1)