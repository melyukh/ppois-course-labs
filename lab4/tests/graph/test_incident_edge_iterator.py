"""IncidentEdgeIterator: g.incident_edges(v).

Допущения: отдаёт и входящие, и исходящие рёбра вершины как кортежи (e_from, e_to);
петель и кратных рёбер нет; порядок не фиксируем. Если у тебя только исходящие —
поправь A_EDGES и модельную функцию expected(). РЕШЕНИЯ помечены в тексте.
"""
import itertools

import pytest

from source.exceptions.badTypeException import BadTypeError
from source.exceptions.nodeDuplicationException import NodeDuplicationError
from source.exceptions.notFoundException import EdgeNotFoundError, NodeNotFoundError

A_EDGES = {("a", "b"), ("a", "c"), ("d", "a")}


@pytest.fixture
def g(build):
    return build("abcde", [
        ("a", "b", 1),     # исходящее из a
        ("a", "c", 2),     # исходящее из a
        ("d", "a", 3),     # входящее в a
        ("b", "c", 4),     # a не касается
    ])                     # e изолирована


def expected(model, v):
    return {(a, b) for a in model for b in model[a] if v in (a, b)}


# ============================ значения ============================

def test_yields_in_and_out_edges(g):
    items = list(g.incident_edges("a"))
    assert set(items) == A_EDGES
    assert len(items) == len(A_EDGES)


def test_elements_are_pairs(g):
    for e in g.incident_edges("a"):
        assert isinstance(e, tuple) and len(e) == 2


def test_direction_preserved(g):
    items = set(g.incident_edges("a"))
    assert ("d", "a") in items        # входящее осталось (d, a), а не (a, d)
    assert ("a", "d") not in items


def test_edges_not_touching_vertex_excluded(g):
    assert ("b", "c") not in set(g.incident_edges("a"))


def test_only_incoming(g):
    assert set(g.incident_edges("d")) == {("d", "a")}


def test_only_outgoing(build):
    g = build("abc", [("a", "b"), ("a", "c")])
    assert set(g.incident_edges("a")) == {("a", "b"), ("a", "c")}


def test_sink_vertex(g):
    assert set(g.incident_edges("c")) == {("a", "c"), ("b", "c")}


def test_isolated_vertex_yields_nothing(g):
    assert list(g.incident_edges("e")) == []


def test_every_yielded_edge_contains_vertex_and_exists(g):
    for v in "abcde":
        for e in g.incident_edges(v):
            assert v in e
            assert g.has_edge(e_from=e[0], e_to=e[1]) is True


def test_count_equals_total_power(g):
    for v in "abcde":
        p = g.node_power(v)
        assert len(list(g.incident_edges(v))) == p["from"] + p["to"]


def test_each_edge_appears_in_incident_of_both_endpoints(g):
    for u, v in g.edges():
        assert (u, v) in set(g.incident_edges(u))
        assert (u, v) in set(g.incident_edges(v))


def test_union_over_all_vertices_is_all_edges(g):
    union = set()
    for v in g.vertices():
        union |= set(g.incident_edges(v))
    assert union == set(g.edges())


def test_sum_of_incident_counts_is_twice_edges(g):
    total = sum(len(list(g.incident_edges(v))) for v in g.vertices())
    assert total == 2 * g.edges_count


def test_opposite_edges_both_listed(build):
    g = build("ab", [("a", "b"), ("b", "a")])
    assert set(g.incident_edges("a")) == {("a", "b"), ("b", "a")}
    assert len(list(g.incident_edges("a"))) == 2


def test_reflects_deleted_edge(g):
    g.delete_edge("d", "a")
    assert set(g.incident_edges("a")) == {("a", "b"), ("a", "c")}
    assert list(g.incident_edges("d")) == []


def test_reflects_deleted_node(g):
    g.delete_node("b")
    assert set(g.incident_edges("a")) == {("a", "c"), ("d", "a")}
    assert set(g.incident_edges("c")) == {("a", "c")}


def test_reflects_added_edge(g):
    g.create_edge("e", "a", 1)
    assert set(g.incident_edges("a")) == A_EDGES | {("e", "a")}
    assert set(g.incident_edges("e")) == {("e", "a")}


def test_recreated_vertex_has_no_old_edges(g):
    g.delete_node("a")
    g.create_node("a")
    assert list(g.incident_edges("a")) == []


@pytest.mark.parametrize("n", [1, 2, 5, 30])
def test_hub_with_many_edges(build, n):
    g = build(range(2 * n + 1), [(0, i) for i in range(1, n + 1)] + [(i, 0) for i in range(n + 1, 2 * n + 1)])
    items = list(g.incident_edges(0))
    assert len(items) == 2 * n
    assert len(set(items)) == 2 * n


# ============================ протокол итератора ============================

def test_iterator_protocol(g):
    it = g.incident_edges("a")
    assert iter(it) is it
    assert hasattr(it, "__next__")


def test_exhausted_iterator_keeps_raising_stop_iteration(g):
    it = g.incident_edges("a")
    list(it)
    for _ in range(3):
        with pytest.raises(StopIteration):
            next(it)


def test_iterator_is_one_shot(g):
    it = g.incident_edges("a")
    list(it)
    assert list(it) == []


def test_empty_iterator_raises_stop_iteration(g):
    with pytest.raises(StopIteration):
        next(g.incident_edges("e"))


def test_next_with_default(g):
    assert next(g.incident_edges("e"), "none") == "none"


def test_new_iterator_each_call(g):
    assert list(g.incident_edges("a")) == list(g.incident_edges("a"))


def test_independent_iterators_same_vertex(g):
    it1, it2 = g.incident_edges("a"), g.incident_edges("a")
    first = next(it1)
    next(it1)
    assert next(it2) == first


def test_independent_iterators_different_vertices(g):
    it_a, it_d = g.incident_edges("a"), g.incident_edges("d")
    next(it_a)
    assert next(it_d) == ("d", "a")
    assert len(list(it_a)) == 2


def test_nested_iteration(g):
    pairs = [(e1, e2) for e1 in g.incident_edges("a") for e2 in g.incident_edges("a")]
    assert len(pairs) == 9


def test_iterating_incident_of_every_vertex_while_iterating_vertices(g):
    total = 0
    for v in g.vertices():
        total += len(list(g.incident_edges(v)))
    assert total == 8


def test_works_with_itertools(g):
    assert len(list(itertools.islice(g.incident_edges("a"), 2))) == 2
    assert set(itertools.chain(g.incident_edges("a"), g.incident_edges("d"))) == A_EDGES


def test_works_with_builtins(g):
    assert sorted(g.incident_edges("a")) == sorted(A_EDGES)
    assert ("a", "b") in g.incident_edges("a")
    assert ("b", "c") not in g.incident_edges("a")
    assert all(len(e) == 2 for e in g.incident_edges("a"))
    assert any(e[0] == "d" for e in g.incident_edges("a"))


def test_partial_consumption_then_rest(g):
    it = g.incident_edges("a")
    first = next(it)
    assert set([first] + list(it)) == A_EDGES


# ============================ неизменность графа ============================

def test_full_iteration_does_not_change_graph(g, fingerprint):
    before = fingerprint(g, "abcdez")
    for v in "abcde":
        list(g.incident_edges(v))
    assert fingerprint(g, "abcdez") == before


def test_partial_iteration_does_not_change_graph(g, fingerprint):
    before = fingerprint(g, "abcdez")
    next(g.incident_edges("a"))
    assert fingerprint(g, "abcdez") == before


def test_node_power_unchanged_by_iteration(g):
    before = g.node_power("a")
    list(g.incident_edges("a"))
    assert g.node_power("a") == before == {"from": 1, "to": 2}


def test_yielded_tuples_are_immutable(g):
    e = next(g.incident_edges("a"))
    with pytest.raises(TypeError):
        e[0] = "zzz"


def test_changing_yielded_list_does_not_affect_graph(g):
    items = list(g.incident_edges("a"))
    items.clear()
    assert set(g.incident_edges("a")) == A_EDGES
    assert g.edges_count == 4


def test_abandoned_iterator_does_not_block_graph(g):
    it = g.incident_edges("a")
    next(it)
    del it
    g.create_edge("e", "a", 1)
    assert g.edges_count == 5


# ============================ исключения графа и итератор ============================

@pytest.mark.parametrize("v", ["zzz", 42, ("t", 1)])
def test_missing_vertex_raises(g, v):
    with pytest.raises(NodeNotFoundError):
        list(g.incident_edges(v))


def test_deleted_vertex_raises(g):
    g.delete_node("a")
    with pytest.raises(NodeNotFoundError):
        list(g.incident_edges("a"))


def test_missing_vertex_does_not_change_graph(g, fingerprint):
    before = fingerprint(g, "abcdez")
    with pytest.raises(NodeNotFoundError):
        list(g.incident_edges("zzz"))
    assert fingerprint(g, "abcdez") == before


def test_delete_all_yielded_incident_edges(g):
    for e in list(g.incident_edges("a")):
        g.delete_edge(*e)
    assert list(g.incident_edges("a")) == []
    assert g.node_power("a") == {"from": 0, "to": 0}
    assert g.edges_count == 1                 # осталось только b->c
    assert g.has_node("a")                    # вершина жива


@pytest.mark.parametrize("edge", sorted(A_EDGES))
def test_double_delete_of_yielded_incident_edge_raises(g, edge):
    assert edge in list(g.incident_edges("a"))
    g.delete_edge(*edge)
    with pytest.raises(EdgeNotFoundError):
        g.delete_edge(*edge)
    assert edge not in set(g.incident_edges("a"))


def test_reverse_of_yielded_edge_is_missing(g):
    assert ("a", "b") in set(g.incident_edges("a"))
    with pytest.raises(EdgeNotFoundError):
        g.delete_edge("b", "a")


def test_deleting_vertex_after_listing_incident_removes_them(g):
    listed = list(g.incident_edges("a"))
    g.delete_node("a")
    for u, v in listed:
        assert g.has_edge(e_from=u, e_to=v) is False
    # РЕШЕНИЕ: допустимо любое из двух «не найдено»; зафиксируй своё
    with pytest.raises((EdgeNotFoundError, NodeNotFoundError)):
        g.delete_edge("a", "b")


def test_create_edge_to_missing_vertex_does_not_add_incident(g):
    with pytest.raises(NodeNotFoundError):
        g.create_edge("a", "zzz", 1)
    assert set(g.incident_edges("a")) == A_EDGES


def test_bad_mass_does_not_add_incident(g):
    with pytest.raises(BadTypeError):
        g.create_edge("a", "e", 1.5)
    assert set(g.incident_edges("a")) == A_EDGES
    assert list(g.incident_edges("e")) == []


def test_duplicate_node_does_not_change_incident(g):
    with pytest.raises(NodeDuplicationError):
        g.create_node("a")
    assert set(g.incident_edges("a")) == A_EDGES


# ============================ изменение графа во время итерации ============================
# РЕШЕНИЕ: любое структурное изменение инвалидирует итератор -> RuntimeError на следующем next().

@pytest.mark.parametrize("mutation", [
    lambda g: g.create_edge("e", "a", 1),
    lambda g: g.delete_edge("a", "c"),
    lambda g: g.delete_node("e"),
    lambda g: g.create_node("z"),
    lambda g: g.delete_node("b"),
], ids=["create_edge", "delete_edge", "delete_isolated", "create_node", "delete_neighbour"])
def test_change_during_iteration_raises(g, mutation):
    it = g.incident_edges("a")
    next(it)
    mutation(g)
    with pytest.raises(RuntimeError):
        next(it)


def test_change_between_creation_and_first_next_raises(g):
    it = g.incident_edges("a")
    g.create_edge("e", "a", 1)
    with pytest.raises(RuntimeError):
        next(it)


def test_deleting_iterated_vertex_during_iteration_raises(g):
    it = g.incident_edges("a")
    next(it)
    g.delete_node("a")
    with pytest.raises(RuntimeError):
        next(it)


def test_new_iterator_works_after_invalidated_one(g):
    it = g.incident_edges("a")
    next(it)
    g.create_edge("e", "a", 1)
    with pytest.raises(RuntimeError):
        next(it)
    assert set(g.incident_edges("a")) == A_EDGES | {("e", "a")}


def test_other_vertex_iterator_also_invalidated(g):
    # РЕШЕНИЕ: версия общая на весь граф, поэтому меняется и чужой итератор
    it = g.incident_edges("d")
    g.create_edge("e", "b", 1)
    with pytest.raises(RuntimeError):
        next(it)


@pytest.mark.parametrize("failing", [
    lambda g: g.create_edge("a", "missing", 1),
    lambda g: g.create_edge("a", "e", "heavy"),
    lambda g: g.delete_edge("a", "e"),
    lambda g: g.delete_node("missing"),
    lambda g: g.create_node("a"),
    lambda g: g.create_node([1]),
], ids=["to_missing", "bad_mass", "missing_edge", "missing_node", "duplicate", "unhashable"])
def test_failed_operation_does_not_invalidate_iterator(g, failing):
    it = g.incident_edges("a")
    first = next(it)
    with pytest.raises((NodeNotFoundError, EdgeNotFoundError, NodeDuplicationError, BadTypeError)):
        failing(g)
    assert set([first] + list(it)) == A_EDGES


# ============================ случайные графы против эталона ============================

@pytest.mark.parametrize("seed", range(10))
def test_random_graph_matches_model(random_graph, seed):
    g, model = random_graph(seed)
    for v in model:
        items = list(g.incident_edges(v))
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
            assert set(g.incident_edges(u)) == expected(model, u)
        with pytest.raises(NodeNotFoundError):
            list(g.incident_edges(v))
