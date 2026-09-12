import pytest
from src.classes.vector import Vector
from typing import Optional, Iterable, Union
from contextlib import nullcontext as does_not_raise


@pytest.mark.parametrize \
(
    "vector1, vector2, expected_result, expected_error", 
    [
        (Vector(1.2, 1.0, 3), Vector(1.5, -1.3, -4.7), (2.7, -0.3, -1.7), does_not_raise()),
        (Vector(1, 2, 3), (1, 3, 2), None, pytest.raises(TypeError,
                                                         match="Неправильный тип данных: переданный аргумент не типа Vector")),
        (Vector(-1, -2, 0), "abracadabra", None, pytest.raises(TypeError,
                                                         match="Неправильный тип данных: переданный аргумент не типа Vector")),
        (12, Vector(-1, -1, -1), None, pytest.raises(TypeError, 
                                                         match="Неправильный тип данных: переданный аргумент не типа Vector"))
    ]
)
def test_adding_and_errors_raising(
    vector1: any,
    vector2: any, 
    expected_result: Optional[tuple[float | int, float | int, float | int]],
    expected_error
) -> None:
    with expected_error:
        vector3 = vector1 + vector2
        assert (vector3.x, vector3.y, vector3.z) == pytest.approx(expected_result, abs=1e-9)


@pytest.mark.parametrize \
(
    "vector1, vector2, expected_result, expected_error",
    [
        (Vector(1, 1, 1), Vector(0, 0, 0), (1, 1, 1), does_not_raise()), 
        (Vector(2.1, -12, 3), Vector(1, -2.3, -3), (1.1, -9.7, 6), does_not_raise()), 
        (Vector(1, 2, 3), (1, 2, 3), None, pytest.raises(TypeError,
                                                         match="Неправильный тип данных: переданный аргумент не типа Vector")), 
        (1, Vector(1, -3, -3), None, pytest.raises(TypeError))
    ]
)
def test_substracting_and_errors_raising(
    vector1: any, 
    vector2: any,
    expected_result: Optional[tuple[float | int, float | int, float | int]],
    expected_error
) -> None:
    with expected_error:
        vector3 = vector1 - vector2
        assert (vector3.x, vector3.y, vector3.z) == pytest.approx(expected_result, abs=1e-9)


@pytest.mark.parametrize \
(
    "vector1_or_num, vector2_or_num, expected_result, expected_error",
    [
        (Vector(1, 2, 3), 2, (2, 4, 6), does_not_raise()),
        (Vector(1.5, -2, 0), 3, (4.5, -6, 0), does_not_raise()),
        (2, Vector(1, 2, 3), (2, 4, 6), does_not_raise()),  # число * вектор

    
        (Vector(1, 2, 3), Vector(4, 5, 6), 32, does_not_raise()),
        (Vector(1, 0, 0), Vector(0, 1, 0), 0, does_not_raise()),

   
        (Vector(1, 2, 3), "abracadabra", None, pytest.raises(TypeError,
                                            match="Неправильный тип данных: переданный аргумент не типа Vector")),
        (Vector(1, 2, 3), [1, 2, 3], None, pytest.raises(TypeError,
                                            match="Неправильный тип данных: переданный аргумент не типа Vector")),
        (Vector(1, 2, 3), None, None, pytest.raises(TypeError,
                                            match="Неправильный тип данных: переданный аргумент не типа Vector")),
    ]
)
def test_multiplication_and_errors_raising(
    vector1_or_num: any,
    vector2_or_num: any,
    expected_result: Union[Optional[tuple[float | int, float | int, float | int]] | Optional[float]],
    expected_error
) -> None:
    with expected_error:
        result = vector1_or_num * vector2_or_num
        if isinstance(result, (float, int)):
            assert result == pytest.approx(expected_result, abs=1e-9)
        else:
            assert (result.x, result.y, result.z) == pytest.approx(expected_result, abs=1e-9)


@pytest.mark.parametrize \
(
    "vector1, vector2, expected_result, expected_error",
    [
        (Vector(1, 0, 0), Vector(0, 1, 0), (0, 0, 1), does_not_raise()),
        (Vector(0, 1, 0), Vector(1, 0, 0), (0, 0, -1), does_not_raise()),
        (Vector(1, 2, 3), Vector(4, 5, 6), (-3, 6, -3), does_not_raise()),
        (Vector(1, 1, 1), Vector(1, 1, 1), (0, 0, 0), does_not_raise()),  # параллельные векторы

        (Vector(1, 2, 3), 5, None, pytest.raises(TypeError,
                                                match="Неправильный тип данных: переданный аргумент не типа Vector")),
        (Vector(1, 2, 3), "abracadabra", None, pytest.raises(TypeError,
                                                match="Неправильный тип данных: переданный аргумент не типа Vector")),
        (Vector(1, 2, 3), (1, 2, 3), None, pytest.raises(TypeError,
                                                match="Неправильный тип данных: переданный аргумент не типа Vector"))
    ]
)
def test_matmultiplication_and_errors_raising(
    vector1: any,
    vector2: any,
    expected_result: Optional[tuple[float | int, float | int, float | int]],
    expected_error
) -> None:
    with expected_error:
        vector3 = vector1 @ vector2
        assert (vector3.x, vector3.y, vector3.z) == pytest.approx(expected_result, abs=1e-9)


@pytest.mark.parametrize \
(
    "vector1, value, expected_result, expected_error",
    [
        (Vector(2, 4, 6), 2, (1, 2, 3), does_not_raise()),
        (Vector(1.5, -3, 0), 3, (0.5, -1, 0), does_not_raise()),
        (Vector(-4, 8, -12), -4, (1, -2, 3), does_not_raise()),
        (Vector(1, 2, 3), 0, None, pytest.raises(ZeroDivisionError,
                                                    match="Нельзя делить на ноль")),
        (Vector(1, 2, 3), "abracadabra", None, pytest.raises(TypeError,
                                                    match="Неправильный тип данных")),
        (Vector(1, 2, 3), Vector(1, 1, 1), None, pytest.raises(TypeError,
                                                    match="Неправильный тип данных")),
        (Vector(1, 2, 3), None, None, pytest.raises(TypeError,
                                                    match="Неправильный тип данных"))
    ]
)
def test_divising_and_errors_raising(
    vector1: any,
    value: any,
    expected_result: Optional[tuple[float | int, float | int, float | int]],
    expected_error
) -> None:
    with expected_error:
            vector3 = vector1 / value
            assert (vector3.x, vector3.y, vector3.z) == pytest.approx(expected_result, abs=1e-9)


@pytest.mark.parametrize \
(
    "vector1, expected_result",
    [
        (Vector(3, 4, 0), 5.0),
        (Vector(1, 0, 0), 1.0),
        (Vector(0, 0, 0), 0.0),
        (Vector(1, 1, 1), 1.7320508075688772),
        (Vector(-3, -4, 0), 5.0),                
        (Vector(2.5, -1.5, 0), 2.9154759474226504),
    ]
)
def test_correct_length_computing(
    vector1: Vector,
    expected_result: float
) -> None:
    assert vector1.length == pytest.approx(expected_result, abs=1e-9)

def test_vector_equality_and_errors_raising() -> None:
    assert Vector(3, 4, 0) == Vector(0, 4, 3)
    assert Vector(1, 0, 0) == Vector(0, 1, 0)
    assert not (Vector(1, 2, 3) == Vector(4, 5, 6))

    assert Vector(1, 0, 0) < Vector(3, 4, 0)
    assert not (Vector(3, 4, 0) < Vector(1, 0, 0))

    assert Vector(3, 4, 0) > Vector(1, 0, 0)
    assert not (Vector(1, 0, 0) > Vector(3, 4, 0))

    invalid_others = ["not a vector", 5, [1, 2, 3], None, {"x": 1}]

    for other in invalid_others:
        with pytest.raises(TypeError, match="Неправильный тип данных: переданный аргумент не типа Vector"):
            Vector(1, 2, 3) == other
        with pytest.raises(TypeError, match="Неправильный тип данных: переданный аргумент не типа Vector"):
            Vector(1, 2, 3) < other
        with pytest.raises(TypeError, match="Неправильный тип данных: переданный аргумент не типа Vector"):
            Vector(1, 2, 3) > other


def test_cos_between_vectors_with_zero_vector_raises():
    v1 = Vector(0, 0, 0)
    v2 = Vector(1, 2, 3)
    with pytest.raises(ZeroDivisionError):
        Vector.cos_between_the_vectors(v1, v2)
