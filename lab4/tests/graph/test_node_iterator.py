"""NodeIterator: iter(g), g.vertices(), reversed(g).

Допущения: отдаёт сами значения вершин; порядок не фиксируем, кроме согласованности
reversed с прямым обходом. РЕШЕНИЯ (поправь, если у тебя иначе) помечены в тексте.
"""
import itertools
from dataclasses import dataclass, field

import pytest

from source.exceptions.badTypeException import BadTypeError
from source.exceptions.nodeDuplicationException import NodeDuplicationError
from source.exceptions.notFoundException import EdgeNotFoundError, NodeNotFoundError


@dataclass(unsafe_hash=True)
class City:
    name: str
    population: int = field(compare=False)


@pytest.fixture
def g(build):
    return build("abcd", [("a", "b"), ("b", "c")])      # d изолирована


@pytest.fixture(params=["iter", "vertices"])
def make(request, g):
    return (lambda: iter(g)) if request.param == "iter" else (lambda: g.vertices())


# ============================ значения ============================

def test_yields_all_nodes_once(make):
    items = list(make())
    assert sorted(items) == ["a", "b", "c", "d"]
    assert len(items) == len(set(items))


def test_empty_graph_yields_nothing(build):
    g = build()
    assert list(iter(g)) == []
    assert list(g.vertices()) == []
    assert list(reversed(g)) == []


def test_isolated_node_included(make):
    assert "d" in list(make())


def test_iter_and_vertices_agree(g):
    assert list(iter(g)) == list(g.vertices())


def test_for_loop_and_list_agree(make):
    assert [v for v in make()] == list(make())


@pytest.mark.parametrize("n", [0, 1, 2, 10, 300])
def test_various_sizes(build, n):
    g = build(range(n))
    assert sorted(g.vertices()) == list(range(n))
    assert sorted(reversed(g)) == list(range(n))


@pytest.mark.parametrize(
    "values",
    [[1, 2, 3], ["x", "y"], [(1, "a"), (2, "b")], [frozenset({1}), frozenset({2})],
     [1, "a", (1, 2), 2.5]],
    ids=["int", "str", "tuple", "frozenset", "mixed"],
)
def test_various_node_types(build, values):
    g = build(values)
    assert len(list(g.vertices())) == len(values)
    assert all(v in values for v in g.vertices())


def test_returns_stored_node_object(build):
    city = City("Minsk", 1)
    g = build([city])
    assert next(g.vertices()) is city


def test_equal_keys_give_single_element(build):
    g = build([1])
    with pytest.raises(NodeDuplicationError):
        g.create_node(1.0)
    assert list(g.vertices()) == [1]


def test_new_iterator_sees_added_nodes(g):
    g.create_node("z")
    assert sorted(g.vertices()) == ["a", "b", "c", "d", "z"]


def test_new_iterator_sees_deleted_nodes(g):
    g.delete_node("a")
    assert sorted(g.vertices()) == ["b", "c", "d"]


def test_recreated_node_appears_once(g):
    g.delete_node("a")
    g.create_node("a")
    assert sorted(g.vertices()) == ["a", "b", "c", "d"]


def test_count_matches_nodes_count(g, make):
    assert len(list(make())) == g.nodes_count


# ============================ протокол итератора ============================

def test_iterator_protocol(make):
    it = make()
    assert iter(it) is it
    assert hasattr(it, "__next__")


def test_exhausted_iterator_keeps_raising_stop_iteration(make):
    it = make()
    list(it)
    for _ in range(3):
        with pytest.raises(StopIteration):
            next(it)


def test_iterator_is_one_shot(make):
    it = make()
    list(it)
    assert list(it) == []


def test_next_with_default_after_exhaustion(make):
    it = make()
    list(it)
    assert next(it, "sentinel") == "sentinel"


def test_empty_graph_next_raises_stop_iteration(build):
    with pytest.raises(StopIteration):
        next(build().vertices())


def test_new_iterator_each_call_starts_from_beginning(g):
    assert list(g.vertices()) == list(g.vertices()) == list(iter(g))


def test_independent_iterators(g):
    it1, it2 = g.vertices(), g.vertices()
    first = next(it1)
    next(it1)
    assert next(it2) == first


def test_interleaved_iterators_give_full_result(g):
    it1, it2 = g.vertices(), g.vertices()
    r1, r2 = [], []
    for _ in range(4):
        r1.append(next(it1))
        r2.append(next(it2))
    assert r1 == r2
    assert sorted(r1) == ["a", "b", "c", "d"]


def test_nested_iteration_over_same_graph(g):
    pairs = [(a, b) for a in g.vertices() for b in g.vertices()]
    assert len(pairs) == 16
    assert len(set(pairs)) == 16


def test_works_with_itertools(g):
    assert len(list(itertools.islice(g.vertices(), 2))) == 2
    assert len(list(itertools.chain(g.vertices(), g.vertices()))) == 8


def test_works_with_builtins(g, make):
    assert sorted(make()) == ["a", "b", "c", "d"]
    assert set(make()) == {"a", "b", "c", "d"}
    assert all(isinstance(v, str) for v in make())
    assert any(v == "c" for v in make())
    assert list(enumerate(sorted(make())))[0] == (0, "a")
    assert "c" in make()
    assert "zzz" not in make()


def test_partial_consumption_then_rest(g):
    it = g.vertices()
    head = [next(it), next(it)]
    tail = list(it)
    assert sorted(head + tail) == ["a", "b", "c", "d"]


# ============================ reversed ============================

def test_reversed_is_reverse_of_forward(g):
    assert list(reversed(g)) == list(iter(g))[::-1]


def test_reversed_yields_all_nodes_once(g):
    items = list(reversed(g))
    assert sorted(items) == ["a", "b", "c", "d"]
    assert len(items) == len(set(items))


@pytest.mark.parametrize("n", [0, 1, 2, 7])
def test_reversed_sizes(build, n):
    g = build(range(n))
    assert list(reversed(g)) == list(iter(g))[::-1]


def test_reversed_is_iterator_and_one_shot(g):
    it = reversed(g)
    assert iter(it) is it
    list(it)
    with pytest.raises(StopIteration):
        next(it)
    assert list(it) == []


def test_reversed_first_is_forward_last(g):
    forward = list(iter(g))
    assert next(reversed(g)) == forward[-1]


def test_reversed_partial_consumption(g):
    forward = list(iter(g))
    assert list(itertools.islice(reversed(g), 2)) == forward[::-1][:2]


def test_reversed_independent_from_forward(g):
    fwd, rev = iter(g), reversed(g)
    f = next(fwd)
    r = next(rev)
    assert f != r
    assert next(fwd) != f


def test_reversed_twice_gives_forward(g):
    assert list(reversed(list(reversed(g)))) == list(iter(g))


def test_reversed_does_not_change_forward_order(g):
    before = list(iter(g))
    list(reversed(g))
    assert list(iter(g)) == before


# ============================ неизменность графа ============================

def test_full_iteration_does_not_change_graph(g, make, fingerprint):
    before = fingerprint(g, "abcdz")
    list(make())
    list(reversed(g))
    assert fingerprint(g, "abcdz") == before


def test_partial_iteration_does_not_change_graph(g, make, fingerprint):
    before = fingerprint(g, "abcdz")
    it = make()
    next(it)
    assert fingerprint(g, "abcdz") == before


def test_nested_iteration_does_not_change_graph(g, fingerprint):
    before = fingerprint(g, "abcdz")
    for _ in g.vertices():
        for _ in reversed(g):
            pass
    assert fingerprint(g, "abcdz") == before


def test_abandoned_iterator_does_not_block_graph(g):
    it = g.vertices()
    next(it)
    del it
    g.create_node("z")
    assert g.nodes_count == 5


def test_changing_yielded_list_does_not_affect_graph(g, make):
    items = list(make())
    items.clear()
    assert g.nodes_count == 4
    assert sorted(make()) == ["a", "b", "c", "d"]


# ============================ исключения графа и итератор ============================

def test_delete_all_yielded_nodes(g):
    for v in list(g.vertices()):          # сначала снимок, потом удаление
        g.delete_node(v)
    assert g.nodes_count == 0
    assert g.edges_count == 0
    assert list(g.vertices()) == []
    assert list(reversed(g)) == []


@pytest.mark.parametrize("v", ["a", "b", "c", "d"])
def test_double_delete_of_yielded_node_raises(g, v):
    assert v in list(g.vertices())
    g.delete_node(v)
    with pytest.raises(NodeNotFoundError):
        g.delete_node(v)


def test_deleted_node_is_not_yielded_and_operations_raise(g):
    g.delete_node("b")
    assert "b" not in list(g.vertices())
    with pytest.raises(NodeNotFoundError):
        g.node_power("b")
    with pytest.raises(NodeNotFoundError):
        list(g.incident_edges("b"))
    with pytest.raises(NodeNotFoundError):
        list(g.adjacent_vertices("b"))


def test_create_edge_with_deleted_node_raises(g):
    g.delete_node("b")
    with pytest.raises(NodeNotFoundError):
        g.create_edge("a", "b", 1)
    assert sorted(g.vertices()) == ["a", "c", "d"]      # вершина b сама не появилась


def test_delete_edge_of_deleted_node_raises(g):
    g.delete_node("a")      # вместе с ней исчезло ребро a->b
    # РЕШЕНИЕ: допустимо любое из двух «не найдено»; зафиксируй своё
    with pytest.raises((EdgeNotFoundError, NodeNotFoundError)):
        g.delete_edge("a", "b")


def test_delete_missing_edge_between_yielded_nodes_raises(g):
    nodes = list(g.vertices())
    assert "a" in nodes and "c" in nodes
    with pytest.raises(EdgeNotFoundError):
        g.delete_edge("a", "c")


def test_create_duplicate_of_yielded_node_raises(g):
    first = next(g.vertices())
    with pytest.raises(NodeDuplicationError):
        g.create_node(first)
    assert g.nodes_count == 4


@pytest.mark.parametrize("bad", [[1], {1}, {"k": 1}, (1, [2])])
def test_unhashable_node_rejected_and_not_iterated(g, bad):
    with pytest.raises(BadTypeError):
        g.create_node(bad)
    assert sorted(g.vertices()) == ["a", "b", "c", "d"]


# ============================ изменение графа во время итерации ============================
# РЕШЕНИЕ: изменение набора вершин инвалидирует итератор -> RuntimeError на следующем next().

@pytest.mark.parametrize("mutation", [
    lambda g: g.create_node("z"),
    lambda g: g.delete_node("d"),
    lambda g: g.delete_node("a"),
], ids=["create_node", "delete_isolated", "delete_with_edges"])
def test_node_change_during_iteration_raises(g, make, mutation):
    it = make()
    next(it)
    mutation(g)
    with pytest.raises(RuntimeError):
        next(it)


@pytest.mark.parametrize("mutation", [
    lambda g: g.create_node("z"),
    lambda g: g.delete_node("d"),
])
def test_node_change_during_reversed_raises(g, mutation):
    it = reversed(g)
    next(it)
    mutation(g)
    with pytest.raises(RuntimeError):
        next(it)


def test_change_between_creation_and_first_next_raises(g):
    it = g.vertices()
    g.create_node("z")
    with pytest.raises(RuntimeError):
        next(it)


def test_new_iterator_works_after_invalidated_one(g, make):
    it = make()
    next(it)
    g.create_node("z")
    with pytest.raises(RuntimeError):
        next(it)
    assert sorted(make()) == ["a", "b", "c", "d", "z"]


def test_invalidated_iterator_keeps_raising(g, make):
    it = make()
    next(it)
    g.create_node("z")
    for _ in range(2):
        with pytest.raises(RuntimeError):
            next(it)


@pytest.mark.parametrize("failing", [
    lambda g: g.create_edge("a", "missing", 1),
    lambda g: g.create_edge("missing", "a", 1),
    lambda g: g.delete_node("missing"),
    lambda g: g.delete_edge("a", "c"),
    lambda g: g.create_node("a"),
    lambda g: g.create_node([1]),
], ids=["edge_to_missing", "edge_from_missing", "delete_missing_node",
        "delete_missing_edge", "duplicate_node", "unhashable"])
def test_failed_operation_does_not_invalidate_iterator(g, make, failing):
    it = make()
    first = next(it)
    with pytest.raises((NodeNotFoundError, EdgeNotFoundError, NodeDuplicationError, BadTypeError)):
        failing(g)
    rest = list(it)                              # итератор жив и отдаёт остаток
    assert sorted([first] + rest) == ["a", "b", "c", "d"]


@pytest.mark.parametrize("mutation", [
    lambda g: g.create_edge("a", "d", 5),
    lambda g: g.delete_edge("a", "b"),
], ids=["create_edge", "delete_edge"])
def test_edge_change_during_node_iteration_raises(g, make, mutation):
    # РЕШЕНИЕ: версия общая на весь граф, поэтому и изменение рёбер инвалидирует итератор вершин.
    # Если хочешь разрешить — замени на проверку, что итератор отдаёт все 4 вершины.
    it = make()
    next(it)
    mutation(g)
    with pytest.raises(RuntimeError):
        next(it)


# ============================ случайные графы против эталона ============================

@pytest.mark.parametrize("seed", range(8))
def test_random_graph_matches_model(random_graph, seed):
    g, model = random_graph(seed)
    assert sorted(g.vertices()) == sorted(model)
    assert sorted(iter(g)) == sorted(model)
    assert list(reversed(g)) == list(iter(g))[::-1]


@pytest.mark.parametrize("seed", range(8))
def test_random_deletions_match_model(random_graph, seed):
    import random
    g, model = random_graph(seed)
    rng = random.Random(seed)
    for v in rng.sample(sorted(model), 5):
        g.delete_node(v)
        del model[v]
        assert sorted(g.vertices()) == sorted(model)
        assert len(list(g.vertices())) == g.nodes_count
