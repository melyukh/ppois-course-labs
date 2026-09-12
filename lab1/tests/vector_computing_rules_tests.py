import pytest
from src.classes.vector import Vector


@pytest.mark.parametrize(
    "vector1, vector2, vector3",
    [
        (Vector(1, 2, 3), Vector(4, 5, 6), Vector(7, 8, 9)),
        (Vector(-1, -2, -3), Vector(4, -5, 6), Vector(0, 0, 0)),
        (Vector(0.5, 1.5, -2.5), Vector(3.3, -1.1, 2.2), Vector(-4, 4, -4))
    ]
)
def test_adding_aksioms(
    vector1: Vector,
    vector2: Vector,
    vector3: Vector
) -> None:
    #коммутативность
    result1, result2 = vector1 + vector2, vector2 + vector1
    assert result1.x == pytest.approx(result2.x)
    assert result1.y == pytest.approx(result2.y)
    assert result1.z == pytest.approx(result2.z)

    #ассоциативность
    result1, result2 = (vector1 + vector2) + vector3, vector1 + (vector2 + vector3)
    assert result1.x == pytest.approx(result2.x)
    assert result1.y == pytest.approx(result2.y)
    assert result1.z == pytest.approx(result2.z)

    #нейтральный элемент (нулевой вектор)
    result = vector1 + Vector(0, 0, 0)
    assert result.x == pytest.approx(vector1.x)
    assert result.y == pytest.approx(vector1.y)
    assert result.z == pytest.approx(vector1.z)

    #обратный элемент
    result = vector1 + (-vector1)
    assert result.x == pytest.approx(0.0)
    assert result.y == pytest.approx(0.0)
    assert result.z == pytest.approx(0.0)


@pytest.mark.parametrize(
    "vector1, vector2, scalar1, scalar2",
    [
        (Vector(1, 2, 3), Vector(4, 5, 6), 2, 3),
        (Vector(-1, 0, 2), Vector(3, -3, 1), -2, 0.5),
        (Vector(0.5, 1.5, -2.5), Vector(2, 2, 2), 4, -1)
    ]
)
def test_multiplying_on_scalar_aksioms(
    vector1: Vector,
    vector2: Vector,
    scalar1: float | int,
    scalar2: float | int
) -> None:
    #дистрибутивность относительно сложения векторов
    result1, result2 = scalar1 * (vector1 + vector2), scalar1 * vector1 + scalar1 * vector2
    assert result1.x == pytest.approx(result2.x)
    assert result1.y == pytest.approx(result2.y)
    assert result1.z == pytest.approx(result2.z)

    #дистрибутивность относительно сложения скаляров
    result1, result2 = (scalar1 + scalar2) * vector1, scalar1 * vector1 + scalar2 * vector1
    assert result1.x == pytest.approx(result2.x)
    assert result1.y == pytest.approx(result2.y)
    assert result1.z == pytest.approx(result2.z)

    #ассоциативность скаляров
    result1, result2 = scalar1 * (scalar2 * vector1), (scalar1 * scalar2) * vector1
    assert result1.x == pytest.approx(result2.x)
    assert result1.y == pytest.approx(result2.y)
    assert result1.z == pytest.approx(result2.z)

    #нейтральный элемент
    result = 1 * vector1
    assert result.x == pytest.approx(vector1.x)
    assert result.y == pytest.approx(vector1.y)
    assert result.z == pytest.approx(vector1.z)

    #умножение на 0
    result = 0 * vector1
    assert result.x == pytest.approx(0.0)
    assert result.y == pytest.approx(0.0)
    assert result.z == pytest.approx(0.0)


@pytest.mark.parametrize(
    "vector1, vector2, vector3",
    [
        (Vector(1, 2, 3), Vector(4, 5, 6), Vector(7, 8, 9)),
        (Vector(-1, -2, -3), Vector(4, -5, 6), Vector(0, 0, 0)),
        (Vector(0.5, 1.5, -2.5), Vector(3.3, -1.1, 2.2), Vector(-4, 4, -4))
    ]
)
def test_dot_product_aksioms(
    vector1: Vector,
    vector2: Vector,
    vector3: Vector
) -> None:
    #коммутативность
    result1, result2 = vector1 * vector2, vector2 * vector1
    assert result1 == pytest.approx(result2)

    #дистрибутивность
    result1, result2 = vector1 * (vector2 + vector3), vector1 * vector2 + vector1 * vector3
    assert result1 == pytest.approx(result2)

    #связь с длиной вектора
    assert vector1 * vector1 == pytest.approx(vector1.length ** 2)


@pytest.mark.parametrize(
    "vector1, vector2",
    [
        (Vector(1, 0, 0), Vector(0, 1, 0)),
        (Vector(0, 1, 0), Vector(0, 0, 1)),
        (Vector(3, 0, 0), Vector(0, -5, 0))
    ]
)
def test_orthogonality(vector1: Vector, vector2: Vector) -> None:
    #ортогональные векторы -> скалярное произведение равно нулю
    assert vector1 * vector2 == pytest.approx(0.0)


@pytest.mark.parametrize(
    "vector1, vector2, vector3",
    [
        (Vector(1, 2, 3), Vector(4, 5, 6), Vector(7, 8, 9)),
        (Vector(-1, -2, -3), Vector(4, -5, 6), Vector(0, 0, 0)),
        (Vector(0.5, 1.5, -2.5), Vector(3.3, -1.1, 2.2), Vector(-4, 4, -4))
    ]
)
def test_cross_product_aksioms(
    vector1: Vector,
    vector2: Vector,
    vector3: Vector
) -> None:
    #антикоммутативность
    result1, result2 = vector1 @ vector2, -(vector2 @ vector1)
    assert result1.x == pytest.approx(result2.x)
    assert result1.y == pytest.approx(result2.y)
    assert result1.z == pytest.approx(result2.z)

    #дистрибутивность
    result1, result2 = vector1 @ (vector2 + vector3), vector1 @ vector2 + vector1 @ vector3
    assert result1.x == pytest.approx(result2.x)
    assert result1.y == pytest.approx(result2.y)
    assert result1.z == pytest.approx(result2.z)


@pytest.mark.parametrize(
    "vector1, vector2",
    [
        (Vector(1, 2, 3), Vector(2, 4, 6)),
        (Vector(-1, 0, 0), Vector(5, 0, 0)),
        (Vector(0, 0.5, 1), Vector(0, -1, -2))
    ]
)
def test_collinearity(vector1: Vector, vector2: Vector) -> None:
    result = vector1 @ vector2
    assert result.x == pytest.approx(0.0)
    assert result.y == pytest.approx(0.0)
    assert result.z == pytest.approx(0.0)


@pytest.mark.parametrize(
    "vector1, vector2",
    [
        (Vector(1, 2, 3), Vector(4, 5, 6)),
        (Vector(-1, -2, -3), Vector(4, -5, 6)),
        (Vector(0.5, 1.5, -2.5), Vector(3.3, -1.1, 2.2))
    ]
)
def test_cross_product_perpendicular_to_operands(vector1: Vector, vector2: Vector) -> None:
    result = vector1 @ vector2
    assert result * vector1 == pytest.approx(0.0)
    assert result * vector2 == pytest.approx(0.0)


def test_zero_vector_length():
    v = Vector(0, 0, 0)
    assert v.length == pytest.approx(0.0)

@pytest.mark.parametrize(
    "vector",
    [
        Vector(1, 2, 3),
        Vector(-4, 5, -6),
        Vector(0.5, -1.5, 2.5)
    ]
)
def test_cross_product_with_zero_vector(vector: Vector):
    zero = Vector(0, 0, 0)
    result = vector @ zero
    assert result.x == pytest.approx(0.0)
    assert result.y == pytest.approx(0.0)
    assert result.z == pytest.approx(0.0)

#правило треугольника
@pytest.mark.parametrize(
    "vector1, vector2",
    [
        (Vector(1, 2, 3), Vector(4, 5, 6)),
        (Vector(-1, -2, -3), Vector(4, -5, 6)),
        (Vector(0.5, 1.5, -2.5), Vector(3.3, -1.1, 2.2)),
        (Vector(1, 0, 0), Vector(-1, 0, 0))
    ]
)
def test_triangle_inequality(vector1: Vector, vector2: Vector):
    left = (vector1 + vector2).length
    right = vector1.length + vector2.length
    assert left <= right + 1e-9