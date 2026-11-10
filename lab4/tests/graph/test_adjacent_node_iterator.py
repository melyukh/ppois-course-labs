"""AdjacentNodeIterator: g.adjacent_nodes(v).

Семантика: узлы, в которые из v ведёт ребро (ИСХОДЯЩИЕ соседи). Узлы, из которых
ребро идёт в v, не выдаются. Каждый сосед один раз, сама v не входит. Порядок не фиксируем.
РЕШЕНИЯ помечены в тексте.
"""
import itertools

import pytest

from source.exceptions.badTypeException import BadTypeError
from source.exceptions.nodeDuplicationException import NodeDuplicationError
from source.exceptions.notFoundException import EdgeNotFoundError, NodeNotFoundError

A_NEIGHBOURS = {"b", "d"}


@pytest.fixture
def g(build):
    return build("abcde", [
        ("a", "b", 1),     # a -> b
        ("c", "a", 2),     # c -> a: c НЕ сосед a
        ("a", "d", 3),     # a -> d
        ("d", "a", 4),     # встречное: d всё равно один раз
        ("b", "c", 5),
    ])                     # e изолирована


def expected(model, v):
    return set(model[v])


# ============================ значения ============================

def test_yields_all_outgoing_neighbours(g):
    assert set(g.adjacent_nodes("a")) == A_NEIGHBOURS


def test_no_duplicates_for_opposite_edges(g):
    items = list(g.adjacent_nodes("a"))
    assert items.count("d") == 1
    assert len(items) == len(A_NEIGHBOURS)


def test_outgoing_neighbour_included(g):
    assert "b" in set(g.adjacent_nodes("a"))


def test_incoming_only_node_is_not_neighbour(g):
    assert "c" not in set(g.adjacent_nodes("a"))


def test_node_is_not_its_own_neighbour(g):
    for v in "abcde":
        assert v not in set(g.adjacent_nodes(v))


def test_non_adjacent_excluded(g):
    assert "e" not in set(g.adjacent_nodes("a"))


def test_isolated_node_has_no_neighbours(g):
    assert list(g.adjacent_nodes("e")) == []


def test_sink_has_no_neighbours(build):
    g = build("ab", [("a", "b")])
    assert list(g.adjacent_nodes("b")) == []


def test_adjacency_is_not_symmetric(g):
    assert "b" in set(g.adjacent_nodes("a"))
    assert "a" not in set(g.adjacent_nodes("b"))


def test_every_neighbour_is_a_node(g):
    for u in "abcde":
        for v in g.adjacent_nodes(u):
            assert g.has_node(v) is True


def test_neighbour_iff_outgoing_edge(g):
    for u in "abcde":
        nb = set(g.adjacent_nodes(u))
        for v in "abcde":
            assert (v in nb) is g.has_edge(e_from=u, e_to=v)


def test_sum_of_neighbour_counts_equals_edges_count(g):
    total = sum(len(list(g.adjacent_nodes(v))) for v in "abcde")
    assert total == g.edges_count == 5


def test_consistent_with_incident_edges(g):
    for v in "abcde":
        assert set(g.adjacent_nodes(v)) == {w for _, w in g.incident_edges(v)}


@pytest.mark.parametrize("n", [1, 2, 5, 30])
def test_hub_with_many_neighbours(build, n):
    g = build(range(n + 1), [(0, i) for i in range(1, n + 1)])
    assert set(g.adjacent_nodes(0)) == set(range(1, n + 1))
    for i in range(1, n + 1):
        assert list(g.adjacent_nodes(i)) == []


def test_reflects_deleted_edge(g):
    g.delete_edge("a", "b")
    assert set(g.adjacent_nodes("a")) == {"d"}


def test_deleting_incoming_edge_does_not_change_result(g):
    g.delete_edge("c", "a")
    assert set(g.adjacent_nodes("a")) == A_NEIGHBOURS


def test_opposite_edge_does_not_keep_neighbour(g):
    g.delete_edge("a", "d")
    assert "d" not in set(g.adjacent_nodes("a"))      # d->a остался, но a->d нет


def test_reflects_deleted_node(g):
    g.delete_node("d")
    assert set(g.adjacent_nodes("a")) == {"b"}


def test_reflects_added_edge(g):
    g.create_edge("a", "e", 1)
    assert set(g.adjacent_nodes("a")) == A_NEIGHBOURS | {"e"}


def test_added_incoming_edge_does_not_appear(g):
    g.create_edge("e", "a", 1)
    assert set(g.adjacent_nodes("a")) == A_NEIGHBOURS
    assert set(g.adjacent_nodes("e")) == {"a"}


def test_recreated_node_has_no_old_neighbours(g):
    assert "a" in set(g.adjacent_nodes("c"))
    g.delete_node("a")
    g.create_node("a")
    assert list(g.adjacent_nodes("a")) == []
    assert "a" not in set(g.adjacent_nodes("c"))


# ============================ протокол итератора ============================

def test_iterator_protocol(g):
    it = g.adjacent_nodes("a")
    assert iter(it) is it
    assert hasattr(it, "__next__")


def test_exhausted_iterator_keeps_raising_stop_iteration(g):
    it = g.adjacent_nodes("a")
    list(it)
    for _ in range(3):
        with pytest.raises(StopIteration):
            next(it)


def test_iterator_is_one_shot(g):
    it = g.adjacent_nodes("a")
    list(it)
    assert list(it) == []


def test_empty_iterator_raises_stop_iteration(g):
    with pytest.raises(StopIteration):
        next(g.adjacent_nodes("e"))


def test_next_with_default(g):
    assert next(g.adjacent_nodes("e"), "none") == "none"


def test_new_iterator_each_call(g):
    assert list(g.adjacent_nodes("a")) == list(g.adjacent_nodes("a"))


def test_independent_iterators_same_node(g):
    it1, it2 = g.adjacent_nodes("a"), g.adjacent_nodes("a")
    first = next(it1)
    next(it1)
    assert next(it2) == first


def test_independent_iterators_different_nodes(g):
    it_a, it_b = g.adjacent_nodes("a"), g.adjacent_nodes("b")
    next(it_a)
    assert set(it_b) == {"c"}
    assert len(list(it_a)) == 1


def test_nested_iteration(g):
    pairs = [(x, y) for x in g.adjacent_nodes("a") for y in g.adjacent_nodes("a")]
    assert len(pairs) == 4


def test_two_hop_traversal(g):
    # a -> {b, d}; b -> {c}; d -> {a}
    second = {y for x in g.adjacent_nodes("a") for y in g.adjacent_nodes(x)}
    assert second == {"c", "a"}


def test_works_with_itertools(g):
    assert len(list(itertools.islice(g.adjacent_nodes("a"), 1))) == 1
    assert set(itertools.chain(g.adjacent_nodes("a"), g.adjacent_nodes("e"))) == A_NEIGHBOURS


def test_works_with_builtins(g):
    assert sorted(g.adjacent_nodes("a")) == ["b", "d"]
    assert "b" in g.adjacent_nodes("a")
    assert "c" not in g.adjacent_nodes("a")
    assert all(isinstance(v, str) for v in g.adjacent_nodes("a"))
    assert any(v == "d" for v in g.adjacent_nodes("a"))


def test_partial_consumption_then_rest(g):
    it = g.adjacent_nodes("a")
    first = next(it)
    assert set([first] + list(it)) == A_NEIGHBOURS


# ============================ неизменность графа ============================

def test_full_iteration_does_not_change_graph(g, fingerprint):
    before = fingerprint(g, "abcdez")
    for v in "abcde":
        list(g.adjacent_nodes(v))
    assert fingerprint(g, "abcdez") == before


def test_partial_iteration_does_not_change_graph(g, fingerprint):
    before = fingerprint(g, "abcdez")
    next(g.adjacent_nodes("a"))
    assert fingerprint(g, "abcdez") == before


def test_changing_yielded_list_does_not_affect_graph(g):
    items = list(g.adjacent_nodes("a"))
    items.clear()
    assert set(g.adjacent_nodes("a")) == A_NEIGHBOURS


def test_abandoned_iterator_does_not_block_graph(g):
    it = g.adjacent_nodes("a")
    next(it)
    del it
    g.create_edge("e", "a", 1)
    assert g.edges_count == 6


# ============================ исключения графа и итератор ============================

@pytest.mark.parametrize("v", ["zzz", 42, ("t", 1)])
def test_missing_node_raises(g, v):
    with pytest.raises(NodeNotFoundError):
        list(g.adjacent_nodes(v))


def test_deleted_node_raises(g):
    g.delete_node("a")
    with pytest.raises(NodeNotFoundError):
        list(g.adjacent_nodes("a"))


def test_unhashable_node_raises_bad_type(g):
    with pytest.raises(BadTypeError):
        list(g.adjacent_nodes({"k": 1}))


def test_missing_node_does_not_change_graph(g, fingerprint):
    before = fingerprint(g, "abcdez")
    with pytest.raises(NodeNotFoundError):
        list(g.adjacent_nodes("zzz"))
    assert fingerprint(g, "abcdez") == before


def test_every_yielded_neighbour_edge_can_be_deleted(g):
    for v in list(g.adjacent_nodes("a")):
        g.delete_edge("a", v)
    assert list(g.adjacent_nodes("a")) == []
    assert g.edges_count == 3                      # c->a, d->a, b->c


def test_incoming_only_node_edge_cannot_be_deleted_outgoing(g):
    assert "c" not in set(g.adjacent_nodes("a"))
    with pytest.raises(EdgeNotFoundError):
        g.delete_edge("a", "c")


def test_reverse_of_yielded_edge_cannot_be_deleted_for_one_way(g):
    assert "b" in set(g.adjacent_nodes("a"))
    with pytest.raises(EdgeNotFoundError):
        g.delete_edge("b", "a")


def test_delete_every_neighbour_node(g):
    for v in list(g.adjacent_nodes("a")):
        g.delete_node(v)
    assert list(g.adjacent_nodes("a")) == []
    assert sorted(g.nodes()) == ["a", "c", "e"]


@pytest.mark.parametrize("v", sorted(A_NEIGHBOURS))
def test_double_delete_of_yielded_neighbour_raises(g, v):
    assert v in list(g.adjacent_nodes("a"))
    g.delete_node(v)
    with pytest.raises(NodeNotFoundError):
        g.delete_node(v)
    with pytest.raises(NodeNotFoundError):
        g.create_edge("a", v, 1)
    assert v not in set(g.adjacent_nodes("a"))


def test_create_edge_to_missing_node_does_not_add_neighbour(g):
    with pytest.raises(NodeNotFoundError):
        g.create_edge("a", "zzz", 1)
    assert set(g.adjacent_nodes("a")) == A_NEIGHBOURS


def test_bad_mass_does_not_add_neighbour(g):
    with pytest.raises(BadTypeError):
        g.create_edge("a", "e", None)
    assert "e" not in set(g.adjacent_nodes("a"))


def test_duplicate_node_does_not_change_neighbours(g):
    with pytest.raises(NodeDuplicationError):
        g.create_node("b")
    assert set(g.adjacent_nodes("a")) == A_NEIGHBOURS


# ============================ изменение графа во время итерации ============================
# РЕШЕНИЕ: любое структурное изменение инвалидирует итератор -> RuntimeError на следующем next().

@pytest.mark.parametrize("mutation", [
    lambda g: g.create_edge("e", "a", 1),
    lambda g: g.delete_edge("a", "b"),
    lambda g: g.delete_node("e"),
    lambda g: g.create_node("z"),
    lambda g: g.delete_node("b"),
], ids=["create_edge", "delete_edge", "delete_isolated", "create_node", "delete_neighbour"])
def test_change_during_iteration_raises(g, mutation):
    it = g.adjacent_nodes("a")
    next(it)
    mutation(g)
    with pytest.raises(RuntimeError):
        next(it)


def test_change_between_creation_and_first_next_raises(g):
    it = g.adjacent_nodes("a")
    g.create_edge("e", "a", 1)
    with pytest.raises(RuntimeError):
        next(it)


def test_deleting_iterated_node_during_iteration_raises(g):
    it = g.adjacent_nodes("a")
    next(it)
    g.delete_node("a")
    with pytest.raises(RuntimeError):
        next(it)


def test_new_iterator_works_after_invalidated_one(g):
    it = g.adjacent_nodes("a")
    next(it)
    g.create_edge("a", "e", 1)
    with pytest.raises(RuntimeError):
        next(it)
    assert set(g.adjacent_nodes("a")) == A_NEIGHBOURS | {"e"}


@pytest.mark.parametrize("failing", [
    lambda g: g.create_edge("a", "missing", 1),
    lambda g: g.create_edge("a", "e", "heavy"),
    lambda g: g.delete_edge("a", "e"),
    lambda g: g.delete_node("missing"),
    lambda g: g.create_node("a"),
    lambda g: g.create_node([1]),
], ids=["to_missing", "bad_mass", "missing_edge", "missing_node", "duplicate", "unhashable"])
def test_failed_operation_does_not_invalidate_iterator(g, failing):
    it = g.adjacent_nodes("a")
    first = next(it)
    with pytest.raises((NodeNotFoundError, EdgeNotFoundError, NodeDuplicationError, BadTypeError)):
        failing(g)
    assert set([first] + list(it)) == A_NEIGHBOURS


# ============================ случайные графы против эталона ============================

@pytest.mark.parametrize("seed", range(10))
def test_random_graph_matches_model(random_graph, seed):
    g, model = random_graph(seed)
    for v in model:
        items = list(g.adjacent_nodes(v))
        assert set(items) == expected(model, v)
        assert len(items) == len(set(items))


@pytest.mark.parametrize("seed", range(10))
def test_random_deletions_match_model(random_graph, seed):
    import random
    g, model = random_graph(seed)
    rng = random.Random(seed)
    for v in rng.sample(sorted(model), 4):
        g.delete_node(v)
        del model[v]
        for out in model.values():
            out.pop(v, None)
        for u in model:
            assert set(g.adjacent_nodes(u)) == expected(model, u)
        with pytest.raises(NodeNotFoundError):
            list(g.adjacent_nodes(v))
