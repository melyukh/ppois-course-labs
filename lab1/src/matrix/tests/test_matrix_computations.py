import math
import pytest
from src.matrix.classes.matrix import Matrix


@pytest.mark.parametrize(
    "data1, data2, expected",
    [
        ([[1, 2], [3, 4]], [[5, 6], [7, 8]], [[6, 8], [10, 12]]),
        ([[0, 0], [0, 0]], [[1, 2], [3, 4]], [[1, 2], [3, 4]]),
        ([[-1, -2], [-3, -4]], [[1, 2], [3, 4]], [[0, 0], [0, 0]]),
        ([[1, 2, 3]], [[4, 5, 6]], [[5, 7, 9]]),
    ]
)
def test_add_two_matrices(data1, data2, expected):
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
def test_add_matrix_and_number(data, number, expected):
    result = Matrix(data) + number
    assert result.matrix == pytest.approx(expected)


@pytest.mark.parametrize(
    "data1, data2",
    [
        ([[1, 2], [3, 4]], [[1, 2, 3], [4, 5, 6]]),
        ([[1, 2, 3]], [[1], [2]]),
    ]
)
def test_add_different_sizes_raises(data1, data2):
    with pytest.raises(ValueError):
        Matrix(data1) + Matrix(data2)


@pytest.mark.parametrize("invalid_other", ["строка", None, [1, 2, 3]])
def test_add_invalid_type_raises(invalid_other):
    m = Matrix([[1, 2], [3, 4]])
    with pytest.raises(TypeError):
        m + invalid_other


def test_iadd_creates_correct_result():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[1, 1], [1, 1]])
    m1 += m2
    assert m1.matrix == [[2, 3], [4, 5]]


def test_radd_number_plus_matrix():
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
def test_sub_two_matrices(data1, data2, expected):
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
def test_sub_matrix_and_number(data, number, expected):
    result = Matrix(data) - number
    assert result.matrix == expected


@pytest.mark.parametrize(
    "data1, data2",
    [
        ([[1, 2], [3, 4]], [[1, 2, 3], [4, 5, 6]]),
        ([[1, 2, 3]], [[1], [2]]),
    ]
)
def test_sub_different_sizes_raises(data1, data2):
    with pytest.raises(ValueError):
        Matrix(data1) - Matrix(data2)


def test_isub_creates_correct_result():
    m1 = Matrix([[5, 6], [7, 8]])
    m2 = Matrix([[1, 1], [1, 1]])
    m1 -= m2
    assert m1.matrix == [[4, 5], [6, 7]]


@pytest.mark.parametrize(
    "data1, data2, expected",
    [
        ([[1, 2], [3, 4]], [[5, 6], [7, 8]], [[19, 22], [43, 50]]),
        ([[1, 0], [0, 1]], [[5, 6], [7, 8]], [[5, 6], [7, 8]]),  # умножение на единичную
        ([[2, 0], [0, 2]], [[1, 2], [3, 4]], [[2, 4], [6, 8]]),  # умножение на диагональную
        (
            [[1, 2, 3], [4, 5, 6]],       # 2x3
            [[7, 8], [9, 10], [11, 12]],  # 3x2
            [[58, 64], [139, 154]],
        ),
    ]
)
def test_mul_two_matrices(data1, data2, expected):
    result = Matrix(data1) * Matrix(data2)
    assert result.matrix == expected


@pytest.mark.parametrize(
    "data1, data2",
    [
        ([[1, 2], [3, 4]], [[1, 2, 3], [4, 5, 6], [7, 8, 9]]),  # 2x2 * 3x3
        ([[1, 2, 3]], [[1, 2, 3]]),                              # 1x3 * 1x3
    ]
)
def test_mul_incompatible_sizes_raises(data1, data2):
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
def test_mul_matrix_and_number(data, number, expected):
    result = Matrix(data) * number
    assert result.matrix == pytest.approx(expected)


@pytest.mark.parametrize("number", [3, 0, -2, 0.5])
def test_rmul_number_and_matrix(number):
    m = Matrix([[1, 2], [3, 4]])
    assert (number * m).matrix == (m * number).matrix


def test_imul_with_number():
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
def test_truediv_by_number(data, number, expected):
    result = Matrix(data) / number
    assert result.matrix == pytest.approx(expected)


def test_truediv_by_zero_raises():
    m = Matrix([[1, 2], [3, 4]])
    with pytest.raises(ZeroDivisionError):
        m / 0


@pytest.mark.parametrize("invalid_other", ["строка", None, Matrix([[1, 2], [3, 4]])])
def test_truediv_invalid_type_raises(invalid_other):
    m = Matrix([[1, 2], [3, 4]])
    with pytest.raises(TypeError):
        m / invalid_other


def test_itruediv():
    m = Matrix([[2, 4], [6, 8]])
    m /= 2
    assert m.matrix == [[1, 2], [3, 4]]


@pytest.mark.parametrize(
    "data, power, expected",
    [
        ([[1, 2], [3, 4]], 0, [[1, 0], [0, 1]]),
        ([[1, 2], [3, 4]], 1, [[1, 2], [3, 4]]),
        ([[1, 1], [0, 1]], 3, [[1, 3], [0, 1]]),
        ([[2, 0], [0, 2]], 3, [[8, 0], [0, 8]]),
        ([[1, 0], [0, 1]], 5, [[1, 0], [0, 1]]),  # единичная в любой степени
    ]
)
def test_pow(data, power, expected):
    result = Matrix(data) ** power
    assert result.matrix == pytest.approx(expected)


@pytest.mark.parametrize(
    "data",
    [
        [[1, 2], [3, 4]],
        [[2, 1], [1, 2]],
        [[1, 0, 0], [0, 2, 0], [0, 0, 3]],
    ]
)
def test_pow_two_equals_self_times_self(data):
    m = Matrix(data)
    assert (m ** 2).matrix == pytest.approx((m * m).matrix)


@pytest.mark.parametrize("power", [-1, -5])
def test_pow_negative_raises(power):
    m = Matrix([[1, 2], [3, 4]])
    with pytest.raises(ValueError):
        m ** power


def test_pow_non_square_raises():
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    with pytest.raises(ValueError):
        m ** 2


@pytest.mark.parametrize(
    "data, expected",
    [
        ([[1, 2], [3, 4]], -2),
        ([[2, 0], [0, 2]], 4),
        ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 1),
        ([[2, 1, 1], [4, 3, 3], [8, 7, 9]], 4),
        ([[0, 1], [1, 0]], -1),          # требует перестановки строк
        ([[0, 0], [0, 0]], 0),           # вырожденная (нулевая)
        ([[1, 2], [2, 4]], 0),           # вырожденная (пропорциональные строки)
        ([[5]], 5),                       # 1x1
        ([[2, 0, 0], [0, 3, 0], [0, 0, 4]], 24),  # диагональная
    ]
)
def test_determinant(data, expected):
    assert Matrix(data).determinant() == pytest.approx(expected)


def test_determinant_does_not_mutate_original():
    m = Matrix([[2, 1, 1], [4, 3, 3], [8, 7, 9]])
    original = [row[:] for row in m.matrix]
    m.determinant()
    assert m.matrix == original


def test_determinant_non_square_raises():
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    with pytest.raises(ValueError):
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
def test_norm(data, expected):
    assert Matrix(data).norm() == pytest.approx(expected)


@pytest.mark.parametrize(
    "data",
    [
        [[1, 2], [3, 4]],
        [[-1, -2], [-3, -4]],
        [[0, 0], [0, 0]],
    ]
)
def test_norm_non_negative(data):
    assert Matrix(data).norm() >= 0


@pytest.mark.parametrize(
    "diagonal_values",
    [
        [2, 3, 4],
        [1, 1, 1],
        [-1, 5, -2],
    ]
)
def test_determinant_matches_diagonal_shortcut(diagonal_values):
    n = len(diagonal_values)
    data = [[diagonal_values[i] if i == j else 0 for j in range(n)] for i in range(n)]
    expected = math.prod(diagonal_values)
    assert Matrix(data).determinant() == pytest.approx(expected)
