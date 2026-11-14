import random
from dataclasses import dataclass, field

import pytest

from source.graph.oGraphAdjList import OGraphAdjacencyList            # поправь путь под свою структуру
from source.exceptions.badTypeException import BadTypeError   # поправь путь под свою структуру
from source.exceptions.notFoundException import NodeNotFoundError, EdgeNotFoundError
from source.exceptions.nodeDuplicationException import NodeDuplicationError
# --- Исключения графа: пока общий Exception, подставь свои классы, когда они появятся ---

# --- Ключи словаря, который возвращает node_power: поправь под свои ---
IN_KEY, OUT_KEY = "from", "to"


@dataclass(unsafe_hash=True)
class City:
    name: str                                   # ключ: участвует в __eq__ и __hash__
    population: int = field(compare=False)      # данные: в сравнение и хеш не входят


@pytest.fixture
def graph() -> OGraphAdjacencyList:
    return OGraphAdjacencyList()


@pytest.fixture
def triangle() -> OGraphAdjacencyList:
    """a -> b (1), b -> c (2), c -> a (3)"""
    g = OGraphAdjacencyList()
    for v in "abc":
        g.create_node(v)
    g.create_edge("a", "b", 1)
    g.create_edge("b", "c", 2)
    g.create_edge("c", "a", 3)
    return g


# =========================== Создание ===========================

def test_new_graph_is_empty(graph):
    assert graph.nodes_count == 0
    assert graph.edges_count == 0


def test_graphs_do_not_share_state():
    g1, g2 = OGraphAdjacencyList(), OGraphAdjacencyList()
    g1.create_node(1)
    assert g2.has_node(1) is False
    assert g2.nodes_count == 0


# =========================== Вершины ===========================

def test_create_node(graph):
    graph.create_node("a")
    assert graph.has_node("a") is True
    assert graph.nodes_count == 1


def test_has_node_false_for_missing(graph):
    graph.create_node("a")
    assert graph.has_node("b") is False


@pytest.mark.parametrize(
    "value",
    [1, "a", 2.5, (1, "x"), frozenset({1, 2}), City("Minsk", 1)],
    ids=["int", "str", "float", "tuple", "frozenset", "dataclass"],
)
def test_any_hashable_type_as_node(graph, value):
    graph.create_node(value)
    assert graph.has_node(value) is True
    assert graph.nodes_count == 1


def test_nodes_with_equal_key_are_same_node(graph):
    graph.create_node(City("Minsk", 1))
    assert graph.has_node(City("Minsk", 999)) is True    # population не входит в ключ


def test_equal_values_of_different_types_collapse(graph):
    # особенность Python: 1 == 1.0 == True, и хеши у них совпадают
    graph.create_node(1)
    assert graph.has_node(1.0) is True
    assert graph.has_node(True) is True


# =========================== Рёбра ===========================

def test_create_edge(graph):
    graph.create_node("a")
    graph.create_node("b")
    graph.create_edge("a", "b", 5)
    assert graph.has_edge(e_from="a", e_to="b") is True
    assert graph.edges_count == 1


def test_edge_is_directed(graph):
    graph.create_node("a")
    graph.create_node("b")
    graph.create_edge("a", "b", 5)
    assert graph.has_edge(e_from="b", e_to="a") is False


def test_opposite_edges_are_different_edges(graph):
    graph.create_node("a")
    graph.create_node("b")
    graph.create_edge("a", "b", 1)
    graph.create_edge("b", "a", 2)
    assert graph.edges_count == 2


def test_has_edge_false_for_unknown_nodes(graph):
    assert graph.has_edge(e_from="x", e_to="y") is False


def test_delete_edge(triangle):
    triangle.delete_edge("a", "b")
    assert triangle.has_edge(e_from="a", e_to="b") is False
    assert triangle.has_edge(e_from="b", e_to="c") is True    # остальные рёбра на месте
    assert triangle.edges_count == 2
    assert triangle.nodes_count == 3                          # вершины не тронуты


# =========================== Удаление вершины ===========================

def test_delete_node_removes_incident_edges(triangle):
    triangle.delete_node("b")       # исчезли a->b (входящее) и b->c (исходящее)
    assert triangle.has_node("b") is False
    assert triangle.nodes_count == 2
    assert triangle.edges_count == 1
    assert triangle.has_edge(e_from="c", e_to="a") is True


def test_deleted_node_leaves_no_phantom_edges(triangle):
    triangle.delete_node("b")
    triangle.create_node("b")       # та же вершина создаётся заново
    assert triangle.has_edge(e_from="a", e_to="b") is False   # входящее ребро не воскресло
    assert triangle.has_edge(e_from="b", e_to="c") is False
    assert triangle.edges_count == 1


# =========================== Степень вершины ===========================

def test_node_power_isolated(graph):
    graph.create_node("a")
    assert graph.node_power("a") == {IN_KEY: 0, OUT_KEY: 0}


def test_node_power_directed(graph):
    for v in "abcd":
        graph.create_node(v)
    graph.create_edge("a", "b", 1)
    graph.create_edge("a", "c", 1)
    graph.create_edge("d", "a", 1)
    assert graph.node_power("a") == {IN_KEY: 1, OUT_KEY: 2}
    assert graph.node_power("b") == {IN_KEY: 1, OUT_KEY: 0}
    assert graph.node_power("d") == {IN_KEY: 0, OUT_KEY: 1}


def test_node_power_ignores_edge_mass(graph):
    graph.create_node("a")
    graph.create_node("b")
    graph.create_edge("a", "b", 100)
    assert graph.node_power("a") == {IN_KEY: 0, OUT_KEY: 1}


# =========================== Счётчики против эталонной модели ===========================

def test_counters_match_reference_model():
    rng = random.Random(42)
    g = OGraphAdjacencyList()
    model: dict[int, dict[int, int]] = {}
    size = 15

    for _ in range(500):
        op = rng.choice(["add_node", "add_edge", "del_edge", "del_node"])

        if op == "add_node":
            v = rng.randrange(size)
            if v in model:
                continue
            g.create_node(v)
            model[v] = {}

        elif op == "add_edge" and model:
            a, b = rng.choice(list(model)), rng.choice(list(model))
            if a == b or b in model[a]:
                continue
            weight = rng.randrange(1, 10)
            g.create_edge(a, b, weight)
            model[a][b] = weight

        elif op == "del_edge":
            edges = [(a, b) for a in model for b in model[a]]
            if not edges:
                continue
            a, b = rng.choice(edges)
            g.delete_edge(a, b)
            del model[a][b]

        elif op == "del_node" and model:
            v = rng.choice(list(model))
            g.delete_node(v)
            del model[v]
            for neighbours in model.values():
                neighbours.pop(v, None)

        assert g.nodes_count == len(model)
        assert g.edges_count == sum(len(n) for n in model.values())

    for a in range(size):
        for b in range(size):
            expected = a in model and b in model[a]
            assert g.has_edge(e_from=a, e_to=b) is expected


# ======================================================================
# РЕШЕНИЯ ПО ПОВЕДЕНИЮ: ниже тесты проверяют то, что ещё не зафиксировано в задании.
# Если у тебя реализовано иначе, правь тест или удаляй, но сначала реши, как должно быть.
# ======================================================================

def test_create_duplicate_node_raises(graph):
    graph.create_node("a")
    with pytest.raises(NodeDuplicationError):
        graph.create_node("a")
    assert graph.nodes_count == 1


@pytest.mark.parametrize(
    "value",
    [[1, 2], {"a": 1}, {1, 2}, (1, [2])],
    ids=["list", "dict", "set", "tuple_with_list"],
)
def test_create_node_unhashable_raises(graph, value):
    with pytest.raises(BadTypeError):
        graph.create_node(value)
    assert graph.nodes_count == 0


def test_create_edge_missing_endpoint_raises(graph):
    graph.create_node("a")
    with pytest.raises(NodeNotFoundError):
        graph.create_edge("a", "b", 1)
    with pytest.raises(NodeNotFoundError):
        graph.create_edge("b", "a", 1)
    assert graph.edges_count == 0
    assert graph.nodes_count == 1       # вершина "b" не создалась сама


@pytest.mark.parametrize("mass", ["1", 1.5, None], ids=["str", "float", "none"])
def test_create_edge_non_int_mass_raises(graph, mass):
    graph.create_node("a")
    graph.create_node("b")
    with pytest.raises(BadTypeError):
        graph.create_edge("a", "b", mass)
    assert graph.edges_count == 0


def test_delete_missing_edge_raises(graph):
    graph.create_node("a")
    graph.create_node("b")
    with pytest.raises(EdgeNotFoundError):
        graph.delete_edge("a", "b")


def test_delete_missing_node_raises(graph):
    with pytest.raises(NodeNotFoundError):
        graph.delete_node("a")


def test_node_power_missing_node_raises(graph):
    with pytest.raises(NodeNotFoundError):
        graph.node_power("a")
