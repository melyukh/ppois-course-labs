import pytest
from src.matrix.classes.matrix import Matrix

def test_constructor_basic():
    m = Matrix([[1, 2], [3, 4]])
    assert m.rows == 2
    assert m.columns == 2
    assert m.matrix == [[1, 2], [3, 4]]


def test_constructor_rectangular():
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    assert m.rows == 2
    assert m.columns == 3


@pytest.mark.parametrize(
    "data",
    [
        [],             
        [[1, 2], [3]],   
    ]
)
def test_constructor_invalid_data_raises(data):
    with pytest.raises((ValueError, IndexError)):
        Matrix(data)


def test_resize_increase_fills_zeros():
    m = Matrix([[1, 2], [3, 4]])
    m.resize(3, 3)
    assert m.rows == 3
    assert m.columns == 3
    assert m.matrix == [[1, 2, 0], [3, 4, 0], [0, 0, 0]]


def test_resize_decrease_truncates():
    m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    m.resize(2, 2)
    assert m.rows == 2
    assert m.columns == 2
    assert m.matrix == [[1, 2], [4, 5]]


def test_resize_mixed_dimensions():
    m = Matrix([[1, 2], [3, 4]])
    m.resize(1, 3)
    assert m.matrix == [[1, 2, 0]]


def test_submatrix_basic():
    m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    sub = m.submatrix(2, 2, 0, 0)
    assert sub.matrix == [[1, 2], [4, 5]]


def test_submatrix_with_offset():
    m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    sub = m.submatrix(2, 2, 1, 1)
    assert sub.matrix == [[5, 6], [8, 9]]


def test_submatrix_out_of_bounds_raises():
    m = Matrix([[1, 2], [3, 4]])
    with pytest.raises(ValueError):
        m.submatrix(3, 3, 0, 0)


def test_submatrix_returns_matrix_instance():
    
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    sub = m.submatrix(1, 1, 0, 0)
    assert isinstance(sub, Matrix)


def test_transpose_square():
    
    m = Matrix([[1, 2], [3, 4]])
    t = m.transpose()
    assert t.matrix == [[1, 3], [2, 4]]


def test_transpose_rectangular():
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    t = m.transpose()
    assert t.rows == 3
    assert t.columns == 2
    assert t.matrix == [[1, 4], [2, 5], [3, 6]]


def test_transpose_twice_gives_original():
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
def test_is_square(data, expected):
    assert Matrix(data).is_square() == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([[0, 0], [0, 0]], True),
        ([[0, 0], [0, 1]], False),
        ([[0, 0, 0]], True),
    ]
)
def test_is_zero(data, expected):
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
def test_is_diagonal(data, expected):
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
def test_is_identity(data, expected):
    assert Matrix(data).is_identity() == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([[1, 2], [2, 1]], True),
        ([[1, 2], [3, 1]], False),
        ([[1, 2, 3], [2, 4, 5], [3, 5, 6]], True),
    ]
)
def test_is_symmetric(data, expected):
    assert Matrix(data).is_symmetric() == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([[1, 2], [0, 4]], True),
        ([[1, 2], [3, 4]], False),
        ([[1, 2, 3], [0, 4, 5], [0, 0, 6]], True),
    ]
)
def test_is_high_triangular(data, expected):
    assert Matrix(data).is_high_triangular() == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([[1, 0], [3, 4]], True),
        ([[1, 2], [3, 4]], False),
        ([[1, 0, 0], [2, 3, 0], [4, 5, 6]], True),
    ]
)
def test_is_low_triangular(data, expected):
    assert Matrix(data).is_low_triangular() == expected


def test_eq_same_values():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[1, 2], [3, 4]])
    assert m1 == m2


def test_eq_different_values():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[1, 2], [3, 5]])
    assert m1 != m2


def test_eq_different_sizes():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[1, 2, 3], [4, 5, 6]])
    assert m1 != m2


def test_eq_with_non_matrix_raises():
    m1 = Matrix([[1, 2], [3, 4]])
    with pytest.raises(TypeError):
        m1 == 5
