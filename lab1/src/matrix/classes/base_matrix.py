from abc import ABC
from typing import List, Any

class BaseMatrix(ABC):
    def __init__(self, 
                 two_dim_array: List[List[float]]
                ) -> None:
        self.matrix = two_dim_array
        self.rows = len(two_dim_array)
        self.columns = len(two_dim_array[0])

    def _build(self, data: List[List[float]]) -> "BaseMatrix":
        return type(self)(data)
    
    @staticmethod
    def _is_matrix(other_object: Any) -> bool:
        return isinstance(other_object, BaseMatrix)
    
    @staticmethod
    def _is_num(other_object: Any) -> bool:
        return isinstance(other_object, (float, int))

    def __eq__(self, other):
        if not BaseMatrix._is_matrix(other):
            raise TypeError("сравниваем не с матрицей\n")
        if self.rows != other.rows or self.columns != other.columns:
            return False
        for i in range(self.rows):
            for j in range(self.columns):
                if self.matrix[i][j] != other.matrix[i][j]:
                    return False
        return True

    __hash__ = None

    def resize(self, rows: int, columns: int) -> None:
        new_data = [[0.0] * columns for _ in range(rows)]
    
        for i in range(min(self.rows, rows)):
            for j in range(min(self.columns, columns)):
                new_data[i][j] = self.matrix[i][j]
    
        self.matrix = new_data
        self.rows = rows
        self.columns = columns

    def submatrix(self, 
                  rows: int, 
                  columns: int, 
                  rows_stamp: int, 
                  columns_stamp: int
                 ) -> "BaseMatrix":
        if (rows + rows_stamp - 1 >= self.rows or \
             columns + columns_stamp - 1 >= self.columns):
            raise ValueError("некорректные размеры заданные для подмассива: поиск выйдет за границу индекса\n")

        new_data = [row[columns_stamp: columns_stamp + columns] for row in self.matrix[rows_stamp: rows_stamp + rows]]
        return self._build(new_data)  

    def transpose(self) -> "BaseMatrix":
        new_data = []
        for j in range(self.columns):
            array = []
            for i in range(self.rows):
                array.append(self.matrix[i][j])
            new_data.append(array)

        return self._build(new_data) 


    def is_identity(self) -> bool:
        return self.is_diagonal() and all(self.matrix[i][i] == 1 for i in range(self.rows))

    def is_diagonal(self) -> bool:
        return self.is_low_triangular() and self.is_high_triangular()

    def is_symmetry(self) -> bool:
        return self.is_square() and self == self.transpose()

    def is_low_triangular(self) -> bool:
        if not self.is_square():
            return False
        return all \
        (
            self.matrix[i][j] == 0
            for i in range(self.rows)
            for j in range(i + 1, self.columns)
        )

    def is_high_triangular(self) -> bool:
        if not self.is_square():
            return False
        return all \
        (
            self.matrix[i][j] == 0
            for i in range(self.rows)
            for j in range(i)
        )

    def is_square(self) -> bool:
        return self.rows == self.columns

    def is_zero(self) -> bool:
        return all(self.matrix[i][j] == 0 for i in range(self.rows) for j in range(self.columns))
