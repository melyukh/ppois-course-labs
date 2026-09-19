import copy
import pytest
from src.matrix.classes.matrix import Matrix


def test_generate_from_string_basic() -> None:
    m = Matrix.generate_from_string("1 2\n3 4")
    assert m.matrix == [[1.0, 2.0], [3.0, 4.0]]


def test_generate_from_string_rectangular() -> None:
    m = Matrix.generate_from_string("1 2 3\n4 5 6")
    assert m.rows == 2
    assert m.columns == 3


def test_generate_from_string_invalid_rows_raises() -> None:
    with pytest.raises(ValueError):
        Matrix.generate_from_string("1 2\n3 4 5")


def test_generate_from_string_non_numeric_raises() -> None:
    with pytest.raises(ValueError):
        Matrix.generate_from_string("1 два\n3 4")


@pytest.fixture
def matrix_file(tmp_path) -> None:
    file_path = tmp_path / "matrix.txt"
    file_path.write_text("1 2 3\n4 5 6\n7 8 9\n")
    return str(file_path)


def test_generate_from_file_basic(matrix_file) -> None:
    m = Matrix.generate_from_file(matrix_file)
    assert m.matrix == [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]


def test_generate_from_file_not_found_raises() -> None:
    with pytest.raises(FileNotFoundError):
        Matrix.generate_from_file("несуществующий_файл.txt")


def test_generate_from_file_empty_raises(tmp_path) -> None:
    file_path = tmp_path / "empty.txt"
    file_path.write_text("")
    with pytest.raises(ValueError):
        Matrix.generate_from_file(str(file_path))


def test_generate_from_file_uneven_rows_raises(tmp_path) -> None:
    file_path = tmp_path / "bad.txt"
    file_path.write_text("1 2 3\n4 5\n")
    with pytest.raises(ValueError):
        Matrix.generate_from_file(str(file_path))


def test_str_representation_is_string() -> None:
    m = Matrix([[1, 2], [3, 4]])
    assert isinstance(str(m), str)


def test_serialization_round_trip() -> None:
    m = Matrix([[1.0, 2.0], [3.0, 4.0]])
    text = str(m)
    restored = Matrix.generate_from_string(text)
    restored_flattened = []
    flattened = []
    for i in range(m.rows):
        restored_flattened.extend(restored.matrix[i])
        flattened.extend(m.matrix[i])
    assert flattened == pytest.approx(restored_flattened)


def test_serialization_round_trip_rectangular() -> None:
    m = Matrix([[1.5, -2.5, 3.0], [4.0, 5.5, -6.0]])
    text = str(m)
    restored = Matrix.generate_from_string(text)
    assert restored.rows == m.rows
    assert restored.columns == m.columns
    for row_a, row_b in zip(restored.matrix, m.matrix):
        for a, b in zip(row_a, row_b):
            assert a == pytest.approx(b)


def test_create_returns_matrix_for_generic_data() -> None:
    m = Matrix.create([[1, 2], [3, 4]])
    assert isinstance(m, Matrix)


def test_create_returns_identity_matrix() -> None:
    from src.matrix.classes.identity_matrix import IdentityMatrix 
    m = Matrix.create([[1, 0], [0, 1]])
    assert isinstance(m, IdentityMatrix)


def test_create_returns_diagonal_matrix() -> None:
    from src.matrix.classes.diagonal_matrix import DiagonalMatrix 
    m = Matrix.create([[2, 0], [0, 3]])
    assert isinstance(m, DiagonalMatrix)


def test_create_returns_square_matrix_for_non_special_square() -> None:
    from src.matrix.classes.square_matrix import SquareMatrix 
    m = Matrix.create([[1, 2], [3, 4]])
    assert isinstance(m, SquareMatrix)


def test_create_returns_plain_matrix_for_rectangular() -> None:
    m = Matrix.create([[1, 2, 3], [4, 5, 6]])
    assert type(m) is Matrix


def test_copy_creates_new_object_with_equal_values() -> None:
    original = Matrix([[1, 2], [3, 4]])
    copied = copy.copy(original)

    assert copied is not original
    assert copied.matrix == original.matrix


def test_copy_is_independent_from_original() -> None:
    original = Matrix([[1, 2], [3, 4]])
    copied = copy.copy(original)

    copied.matrix[0][0] = 100

    assert original.matrix[0][0] == 1
    assert copied.matrix[0][0] == 100
