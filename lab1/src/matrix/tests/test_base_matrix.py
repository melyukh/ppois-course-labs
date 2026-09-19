import pytest
from src.matrix.classes.matrix import Matrix
from typing import List
from contextlib import nullcontext as does_not_raise

def test_constructor_basic() -> None:
    m = Matrix([[1, 2], [3, 4]])
    assert m.rows == 2
    assert m.columns == 2
    assert m.matrix == [[1, 2], [3, 4]]


def test_constructor_rectangular() -> None:
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    assert m.rows == 2
    assert m.columns == 3


@pytest.mark.parametrize(
    "data, expected_result, expected_error",
    [
        ([], None, pytest.raises(ValueError, match="Матрица не может быть пустой")),             
        ([[1, 2], [3]], None, pytest.raises(ValueError, match="Неравная длина строк")),   
        ([[1, 2, "hui"], [1, 0, -3], [3, -74, 3]], None, pytest.raises(TypeError, match="Все элементы матрицы должны быть числами")),
        ([[2, 3], [4, -7], [6, 7]], [[2, 3], [4, -7], [6, 7]], does_not_raise())
    ]
)
def test_constructor_invalid_data_raises(
    data: List[List[float]], 
    expected_result: List[List[float]], 
    expected_error
) -> None:
    with expected_error:
        matrix = Matrix(data)
        assert matrix.matrix == expected_result


def test_resize_increase_fills_zeros() -> None:
    m = Matrix([[1, 2], [3, 4]])
    m.resize(3, 3)
    assert m.rows == 3
    assert m.columns == 3
    assert m.matrix == [[1, 2, 0], [3, 4, 0], [0, 0, 0]]


def test_resize_decrease_truncates() -> None:
    m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    m.resize(2, 2)
    assert m.rows == 2
    assert m.columns == 2
    assert m.matrix == [[1, 2], [4, 5]]


def test_resize_mixed_dimensions() -> None:
    m = Matrix([[1, 2], [3, 4]])
    m.resize(1, 3)
    assert m.matrix == [[1, 2, 0]]


def test_submatrix_basic() -> None:
    m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    sub = m.submatrix(2, 2, 0, 0)
    assert sub.matrix == [[1, 2], [4, 5]]


def test_submatrix_with_offset() -> None:
    m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    sub = m.submatrix(2, 2, 1, 1)
    assert sub.matrix == [[5, 6], [8, 9]]


def test_submatrix_out_of_bounds_raises() -> None:
    m = Matrix([[1, 2], [3, 4]])
    with pytest.raises(ValueError):
        m.submatrix(3, 3, 0, 0)


def test_submatrix_returns_matrix_instance() -> None:
    
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    sub = m.submatrix(1, 1, 0, 0)
    assert isinstance(sub, Matrix)


def test_transpose_square() -> None:
    
    m = Matrix([[1, 2], [3, 4]])
    t = m.transpose()
    assert t.matrix == [[1, 3], [2, 4]]


def test_transpose_rectangular() -> None:
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    t = m.transpose()
    assert t.rows == 3
    assert t.columns == 2
    assert t.matrix == [[1, 4], [2, 5], [3, 6]]


def test_transpose_twice_gives_original() -> None:
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    assert m.transpose().transpose().matrix == m.matrix


@pytest.mark.parametrize(
    "data, expected",
    [
        ([[1, 2], [3, 4]], True),
        ([[1, 2, 3], [4, 5, 6]], False),
        ([[1]], True),
    ]
)
def test_is_square(
    data: List[List[float]], 
    expected: bool
) -> None:
    assert Matrix(data).is_square() == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([[0, 0], [0, 0]], True),
        ([[0, 0], [0, 1]], False),
        ([[0, 0, 0]], True),
    ]
)
def test_is_zero(
    data: List[List[float]], 
    expected: bool
) -> None:
    assert Matrix(data).is_zero() == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([[1, 0], [0, 2]], True),
        ([[1, 1], [0, 2]], False),
        ([[0, 0], [0, 0]], True),
        ([[1, 2, 3], [4, 5, 6]], False),
    ]
)
def test_is_diagonal(
    data: List[List[float]],
    expected: bool
) -> None:
    assert Matrix(data).is_diagonal() == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([[1, 0], [0, 1]], True),
        ([[1, 0], [0, 2]], False),
        ([[2, 0], [0, 2]], False),
        ([[1]], True),
    ]
)
def test_is_identity(
    data: List[List[float]],
    expected: bool
) -> None:
    assert Matrix(data).is_identity() == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([[1, 2], [2, 1]], True),
        ([[1, 2], [3, 1]], False),
        ([[1, 2, 3], [2, 4, 5], [3, 5, 6]], True),
    ]
)
def test_is_symmetric(
    data: List[List[float]],
    expected: bool
) -> None:
    assert Matrix(data).is_symmetric() == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([[1, 2], [0, 4]], True),
        ([[1, 2], [3, 4]], False),
        ([[1, 2, 3], [0, 4, 5], [0, 0, 6]], True),
    ]
)
def test_is_high_triangular(
    data: List[List[float]], 
    expected: bool
) -> None:
    assert Matrix(data).is_high_triangular() == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([[1, 0], [3, 4]], True),
        ([[1, 2], [3, 4]], False),
        ([[1, 0, 0], [2, 3, 0], [4, 5, 6]], True),
    ]
)
def test_is_low_triangular(
    data: List[List[float]], 
    expected: bool
) -> None:
    assert Matrix(data).is_low_triangular() == expected


def test_eq_same_values() -> None:
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[1, 2], [3, 4]])
    assert m1 == m2


def test_eq_different_values() -> None:
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[1, 2], [3, 5]])
    assert m1 != m2


def test_eq_different_sizes() -> None:
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[1, 2, 3], [4, 5, 6]])
    assert m1 != m2


def test_eq_with_non_matrix_raises() -> None:
    m1 = Matrix([[1, 2], [3, 4]])
    with pytest.raises(TypeError):
        m1 == 5
