import pytest
from src.vector.classes.vector import Vector
from typing import Iterable, Optional, Any
from contextlib import nullcontext as does_not_raise
import copy


#happy-сценарий что все данные читаются для базового конструктора
@pytest.mark.parametrize \
(
    "x, y, z, expected_x, expected_y, expected_z",
    [
        (1.0, 2, 3, 1.0, 2, 3),
        (13, 4, -5, 13, 4, -5),
        (1.4, -2.1, -3.4, 1.4, -2.1, -3.4)
    ]
)
def test_input(
     x: float | int,
     y: float | int,
     z: float | int,
     expected_x: float | int,
     expected_y: float | int,
     expected_z: float | int
    ) -> None:
    vector = Vector(x, y, z)
    assert (vector.x, vector.y, vector.z) == (expected_x, expected_y, expected_z)


#happy-сценарий что все данные читаются для строк
@pytest.mark.parametrize \
(
    "data, expected_x, expected_y, expected_z",
    [
        ("1 2 3", 1.0, 2.0, 3.0),
        ("-2.3 -14 4", -2.3, -14.0, 4.0)
    ]
)
def test_string_input(
     data: str, 
     expected_x: float | int,
     expected_y: float | int, 
     expected_z: float | int
    ) -> None:
    vector = Vector.generate_from_string(data)
    assert (vector.x, vector.y, vector.z) == (expected_x, expected_y, expected_z)


#happy-сценарий что все данные читаются для iterable-объектов
@pytest.mark.parametrize \
(
    "data, expected_x, expected_y, expected_z",
    [
        ([1, 2, 40], 1.0, 2.0, 40.0),
        ((12, -1.2, -5.3), 12.0, -1.2, -5.3),
    ]
)
def test_iterable_obj_input(
     data: Iterable, 
     expected_x: float | int, 
     expected_y: float | int, 
     expected_z: float | int
) -> None:
    vector = Vector.generate_from_iterable(data)
    assert (vector.x, vector.y, vector.z) == (expected_x, expected_y, expected_z)


#проверка отлавливания ошибок при некорректном наборе входных данных
@pytest.mark.parametrize \
(
    "x, y, z, expected_result, expected_error",
    [
        (1, -2.5, 14.7, (1, -2.5, 14.7), does_not_raise()),
        (1, "", 14, None, pytest.raises(TypeError, match="Неправильный тип данных")),
        ((), {}, 14, None, pytest.raises(TypeError, match="Неправильный тип данных"))
    ]
)
def test_input_raising_error(
     x: float | int,
     y: float | int,
     z: float | int,
     expected_result: Optional[tuple[float | int, float | int, float | int]],
     expected_error
) -> None:
    with expected_error:
        vector = Vector(x, y, z)
        assert (vector.x, vector.y, vector.z) == expected_result

#проверка отлавливания ошибок при некорректной строке
@pytest.mark.parametrize \
(
    "data, expected_result ,expected_error",
    [
        ("1.0 20 -34", (1.0, 20.0, -34.0), does_not_raise()),
        ("1 2", None, pytest.raises(ValueError)),
        ("34 -4 -4.0 -10", None, pytest.raises(ValueError))
    ]
)
def test_string_input_raising_error(
     data: str,
     expected_result: Optional[tuple[float | int, float | int, float | int]],
     expected_error,
) -> None:
    with expected_error:
        vector = Vector.generate_from_string(data)
        assert (vector.x, vector.y, vector.z) == expected_result


#проверка отлавливания ошибок при некорректном iterable-объекте
@pytest.mark.parametrize \
(
    "data, expected_result, expected_error",
    [
        ("1.0 2.4 -12", None, pytest.raises(TypeError, match="Ожидается список/кортеж чисел, а не строка")),
        (12, None, pytest.raises(TypeError, match="Неправильный тип данных: передан не Iterable-тип")),
        ([2.0, 3], None, pytest.raises(ValueError, match="Неверное количество аргументов")),
        ((2, 3.4, 5, 7), None, pytest.raises(ValueError, match="Неверное количество аргументов")),
        ((2.9, 2, -1.4), (2.9, 2, -1.4), does_not_raise())
    ]
)
def test_iterable_obj_input_raising_error(
     data: Iterable[float | int],
     expected_result: tuple[float | int, float | int, float | int],
     expected_error
) -> None:
    with expected_error:
        vector = Vector.generate_from_iterable(data)
        assert (vector.x, vector.y, vector.z) == expected_result


# Cериализация vector -> str -> vector
@pytest.mark.parametrize(
    "vector",
    [
        Vector(1, 2, 3),
        Vector(-4, 5, -6),
        Vector(0.5, -1.5, 2.5),
        Vector(0, 0, 0),
    ]
)
def test_serialization_round_trip(vector: Vector):
    text = str(vector)
    restored = Vector.generate_from_string(text)
    assert restored.x == pytest.approx(vector.x)
    assert restored.y == pytest.approx(vector.y)
    assert restored.z == pytest.approx(vector.z)


# Копирование
def test_copy_creates_new_object_with_equal_values():
    original = Vector(1, 2, 3)
    copied = copy.copy(original)

    assert copied is not original
    assert copied.x == pytest.approx(original.x)
    assert copied.y == pytest.approx(original.y)
    assert copied.z == pytest.approx(original.z)


def test_copy_is_independent_from_original():
    original = Vector(1, 2, 3)
    copied = copy.copy(original)

    copied.x = 100

    assert original.x == pytest.approx(1)
    assert copied.x == pytest.approx(100)