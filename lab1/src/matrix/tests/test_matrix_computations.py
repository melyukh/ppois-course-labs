import math
import pytest
from src.matrix.classes.matrix import Matrix
from typing import List
from contextlib import nullcontext as does_not_raise


@pytest.mark.parametrize(
    "data1, data2, expected",
    [
        ([[1, 2], [3, 4]], [[5, 6], [7, 8]], [[6, 8], [10, 12]]),
        ([[0, 0], [0, 0]], [[1, 2], [3, 4]], [[1, 2], [3, 4]]),
        ([[-1, -2], [-3, -4]], [[1, 2], [3, 4]], [[0, 0], [0, 0]]),
        ([[1, 2, 3]], [[4, 5, 6]], [[5, 7, 9]]),
    ]
)
def test_add_two_matrices(
    data1: List[List[float]],
    data2: List[List[float]], 
    expected: List[List[float]]
) -> None:
    result = Matrix(data1) + Matrix(data2)
    assert result.matrix == expected

@pytest.mark.parametrize(
    "data, number, expected",
    [
        ([[1, 2], [3, 4]], 10, [[11, 12], [13, 14]]),
        ([[1, 2], [3, 4]], 0, [[1, 2], [3, 4]]),
        ([[1, 2], [3, 4]], -1, [[0, 1], [2, 3]]),
        ([[1, 2], [3, 4]], 0.5, [[1.5, 2.5], [3.5, 4.5]]),
    ]
)
def test_add_matrix_and_number(
    data: List[List[float]], 
    number: float, expected: 
    List[List[float]]
) -> None:
    result = Matrix(data) + number
    flattened_expected = []
    flattened_result = []
    for i in range(len(data)):
        flattened_expected.extend(expected[i])
        flattened_result.extend(result.matrix[i])
    assert flattened_expected == pytest.approx(flattened_result)


@pytest.mark.parametrize(
    "data1, data2",
    [
        ([[1, 2], [3, 4]], [[1, 2, 3], [4, 5, 6]]),
        ([[1, 2, 3]], [[1], [2]]),
    ]
)
def test_add_different_sizes_raises(
    data1: List[List[float]], 
    data2: List[List[float]]
) -> None:
    with pytest.raises(ValueError):
        Matrix(data1) + Matrix(data2)


@pytest.mark.parametrize(
    "invalid_other", 
    [
        "строка", 
        None, 
        [1, 2, 3]
    ]
)
def test_add_invalid_type_raises(
    invalid_other
) -> None:
    m = Matrix([[1, 2], [3, 4]])
    with pytest.raises(TypeError):
        m + invalid_other


def test_iadd_creates_correct_result() -> None:
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[1, 1], [1, 1]])
    m1 += m2
    assert m1.matrix == [[2, 3], [4, 5]]


def test_radd_number_plus_matrix() -> None:
    m = Matrix([[1, 2], [3, 4]])
    result = 10 + m
    assert result.matrix == [[11, 12], [13, 14]]


@pytest.mark.parametrize(
    "data1, data2, expected",
    [
        ([[5, 6], [7, 8]], [[1, 2], [3, 4]], [[4, 4], [4, 4]]),
        ([[1, 2], [3, 4]], [[1, 2], [3, 4]], [[0, 0], [0, 0]]),
        ([[0, 0], [0, 0]], [[1, 2], [3, 4]], [[-1, -2], [-3, -4]]),
    ]
)
def test_sub_two_matrices(
    data1: List[List[float]], 
    data2: List[List[float]], 
    expected: List[List[float]]
) -> None:
    result = Matrix(data1) - Matrix(data2)
    assert result.matrix == expected


@pytest.mark.parametrize(
    "data, number, expected",
    [
        ([[5, 6], [7, 8]], 1, [[4, 5], [6, 7]]),
        ([[5, 6], [7, 8]], 0, [[5, 6], [7, 8]]),
        ([[5, 6], [7, 8]], -1, [[6, 7], [8, 9]]),
    ]
)
def test_sub_matrix_and_number(
    data: List[List[float]], 
    number: List[List[float]], 
    expected: List[List[float]]
) -> None:
    result = Matrix(data) - number
    assert result.matrix == expected


@pytest.mark.parametrize(
    "data1, data2",
    [
        ([[1, 2], [3, 4]], [[1, 2, 3], [4, 5, 6]]),
        ([[1, 2, 3]], [[1], [2]]),
    ]
)
def test_sub_different_sizes_raises(
    data1: List[List[float]], 
    data2: List[List[float]]
) -> None:
    with pytest.raises(ValueError):
        Matrix(data1) - Matrix(data2)


def test_isub_creates_correct_result() -> None:
    m1 = Matrix([[5, 6], [7, 8]])
    m2 = Matrix([[1, 1], [1, 1]])
    m1 -= m2
    assert m1.matrix == [[4, 5], [6, 7]]


@pytest.mark.parametrize(
    "data1, data2, expected",
    [
        ([[1, 2], [3, 4]], [[5, 6], [7, 8]], [[19, 22], [43, 50]]),
        ([[1, 0], [0, 1]], [[5, 6], [7, 8]], [[5, 6], [7, 8]]),
        ([[2, 0], [0, 2]], [[1, 2], [3, 4]], [[2, 4], [6, 8]]), 
        (
            [[1, 2, 3], [4, 5, 6]], 
            [[7, 8], [9, 10], [11, 12]],
            [[58, 64], [139, 154]],
        ),
    ]
)
def test_mul_two_matrices(
    data1: List[List[float]], 
    data2: List[List[float]], 
    expected: List[List[float]]
) -> None:
    result = Matrix(data1) * Matrix(data2)
    assert result.matrix == expected


@pytest.mark.parametrize(
    "data1, data2",
    [
        ([[1, 2], [3, 4]], [[1, 2, 3], [4, 5, 6], [7, 8, 9]]), 
        ([[1, 2, 3]], [[1, 2, 3]]),                              
    ]
)
def test_mul_incompatible_sizes_raises(
    data1: List[List[float]],
    data2: List[List[float]]
) -> None:
    with pytest.raises(ValueError):
        Matrix(data1) * Matrix(data2)


@pytest.mark.parametrize(
    "data, number, expected",
    [
        ([[1, 2], [3, 4]], 3, [[3, 6], [9, 12]]),
        ([[1, 2], [3, 4]], 0, [[0, 0], [0, 0]]),
        ([[1, 2], [3, 4]], -1, [[-1, -2], [-3, -4]]),
        ([[1, 2], [3, 4]], 0.5, [[0.5, 1.0], [1.5, 2.0]]),
    ]
)
def test_mul_matrix_and_number(
    data: List[List[float]], 
    number: float, 
    expected: List[List[float]]
) -> None:
    matrix = Matrix.create(data)
    result = matrix * number
    flattened_expected = []
    flattened_result = []
    for i in range(matrix.rows):
        flattened_expected.extend(expected[i])
        flattened_result.extend(result.matrix[i])
    assert flattened_expected == pytest.approx(flattened_result)


@pytest.mark.parametrize(
    "number", 
    [3, 0, -2, 0.5]
)
def test_rmul_number_and_matrix(
    number: float
) -> None:
    m = Matrix([[1, 2], [3, 4]])
    assert (number * m).matrix == (m * number).matrix


def test_imul_with_number() -> None:
    m = Matrix([[1, 2], [3, 4]])
    m *= 2
    assert m.matrix == [[2, 4], [6, 8]]


@pytest.mark.parametrize(
    "data, number, expected",
    [
        ([[2, 4], [6, 8]], 2, [[1, 2], [3, 4]]),
        ([[1, 2], [3, 4]], 1, [[1, 2], [3, 4]]),
        ([[1, 2], [3, 4]], -1, [[-1, -2], [-3, -4]]),
        ([[1, 2], [3, 4]], 0.5, [[2, 4], [6, 8]]),
    ]
)
def test_truediv_by_number(
    data: List[List[float]], 
    number: float, 
    expected: List[List[float]]
) -> None:
    matrix = Matrix.create(data)
    result = matrix / number

    flattened_result = []
    flattened_expected = []
    for i in range(matrix.rows):
        flattened_result.extend(result.matrix[i])
        flattened_expected.extend(expected[i])
    assert flattened_result == pytest.approx(flattened_expected)


def test_truediv_by_zero_raises() -> None:
    m = Matrix([[1, 2], [3, 4]])
    with pytest.raises(ZeroDivisionError):
        m / 0


@pytest.mark.parametrize(
    "invalid_other", 
    [
        "строка", 
        None, 
        Matrix([[1, 2], [3, 4]])
    ]
)
def test_truediv_invalid_type_raises(
    invalid_other
) -> None:
    m = Matrix([[1, 2], [3, 4]])
    with pytest.raises(TypeError):
        m / invalid_other

@pytest.mark.parametrize(
    "data, number, expected",
    [
        ([[2, 4], [6, 8]], 2, [[1.0, 2.0], [3.0, 4.0]]),
        ([[1, 2], [3, 4]], 1, [[1.0, 2.0], [3.0, 4.0]]),
        ([[1, 2], [3, 4]], -1, [[-1.0, -2.0], [-3.0, -4.0]]),
        ([[1, 2], [3, 4]], 0.5, [[2.0, 4.0], [6.0, 8.0]]),
    ]
)
def test_itruediv(
    data: List[List[float]], 
    number: float, 
    expected: List[List[float]]
) -> None:
    matrix = Matrix.create(data)
    matrix /= number
    flattened_expected = []
    flattened_result = []
    for i in range(matrix.rows):
        flattened_result.extend(matrix.matrix[i])
        flattened_expected.extend(expected[i])
    assert flattened_result == pytest.approx(flattened_expected)


@pytest.mark.parametrize(
    "data, power, expected",
    [
        ([[1, 2], [3, 4]], 0, [[1, 0], [0, 1]]),
        ([[1, 2], [3, 4]], 1, [[1, 2], [3, 4]]),
        ([[1, 1], [0, 1]], 3, [[1, 3], [0, 1]]),
        ([[2, 0], [0, 2]], 3, [[8, 0], [0, 8]]),
        ([[1, 0], [0, 1]], 5, [[1, 0], [0, 1]]),
    ]
)
def test_pow(
    data: List[List[float]], 
    power: float, 
    expected: List[List[float]]
) -> None:
    result = Matrix.create(data) ** power
    flattened_expected = []
    flattened_result = []
    for i in range(result.rows):
        flattened_expected.extend(expected[i])
        flattened_result.extend(result.matrix[i])
    assert flattened_result == pytest.approx(flattened_expected)


@pytest.mark.parametrize(
    "data",
    [
        [[1, 2], [3, 4]],
        [[2, 1], [1, 2]],
        [[1, 0, 0], [0, 2, 0], [0, 0, 3]],
    ]
)
def test_pow_two_equals_self_times_self(
    data: List[List[float]]
) -> None:
    m = Matrix.create(data)
    powwed = (m ** 2)
    self_times_self = (m * m)

    flattened_expected = []
    flattened_result = []
    for i in range(m.rows):
        flattened_expected.extend(self_times_self.matrix[i])
        flattened_result.extend(powwed.matrix[i])
    assert flattened_result == pytest.approx(flattened_expected)


@pytest.mark.parametrize(   
    "power", 
    [
        -1,
        -5
    ]
)
def test_pow_negative_raises(
    power: int
) -> None:
    m = Matrix.create([[1, 2], [3, 4]])
    with pytest.raises(ValueError, match="степень не может быть ниже 0\n"):
        m ** power


def test_pow_non_square_raises() -> None:
    m = Matrix.create([[1, 2, 3], [4, 5, 6]])
    with pytest.raises(TypeError):
        m ** 2


@pytest.mark.parametrize(
    "data, expected",
    [
        ([[1, 2], [3, 4]], -2),
        ([[2, 0], [0, 2]], 4),
        ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 1),
        ([[2, 1, 1], [4, 3, 3], [8, 7, 9]], 4),
        ([[0, 1], [1, 0]], -1),          
        ([[0, 0], [0, 0]], 0),           
        ([[1, 2], [2, 4]], 0),           
        ([[5]], 5),                     
        ([[2, 0, 0], [0, 3, 0], [0, 0, 4]], 24),
    ]
)
def test_determinant(
    data: List[List[float]], 
    expected: float
) -> None:
    assert Matrix.create(data).determinant() == pytest.approx(expected)


def test_determinant_does_not_mutate_original() -> None:
    m = Matrix.create([[2, 1, 1], [4, 3, 3], [8, 7, 9]])
    original = [row[:] for row in m.matrix]
    m.determinant()
    assert m.matrix == original


def test_determinant_non_square_raises() -> None:
    m = Matrix.create([[1, 2, 3], [4, 5, 6]])
    with pytest.raises(AttributeError):
        m.determinant()


@pytest.mark.parametrize(
    "data, expected",
    [
        ([[3, 4]], 5.0),
        ([[1, 2], [3, 4]], math.sqrt(30)),
        ([[0, 0], [0, 0]], 0.0),
        ([[-1, -2], [-3, -4]], math.sqrt(30)),
        ([[5]], 5.0),
    ]
)
def test_norm(
    data: List[List[float]], 
    expected: float
) -> None:
    assert Matrix.create(data).norm() == pytest.approx(expected)


@pytest.mark.parametrize(
    "data",
    [
        [[1, 2], [3, 4]],
        [[-1, -2], [-3, -4]],
        [[0, 0], [0, 0]],
    ]
)
def test_norm_non_negative(
    data: List[List[float]]
) -> None:
    assert Matrix.create(data).norm() >= 0


@pytest.mark.parametrize(
    "diagonal_values",
    [
        [2, 3, 4],
        [1, 1, 1],
        [-1, 5, -2],
    ]
)
def test_determinant_matches_diagonal_shortcut(
    diagonal_values: List[float]
) -> None:
    n = len(diagonal_values)
    data = [[diagonal_values[i] if i == j else 0 for j in range(n)] for i in range(n)]
    expected = math.prod(diagonal_values)
    assert Matrix.create(data).determinant() == pytest.approx(expected)
