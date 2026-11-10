"""EdgeIterator: g.edges().

Допущения: элемент — кортеж-пара (e_from, e_to) без веса; порядок не фиксируем.
РЕШЕНИЯ (поправь, если у тебя иначе) помечены в тексте.
"""
import itertools

import pytest

from source.exceptions.badTypeException import BadTypeError
from source.exceptions.nodeDuplicationException import NodeDuplicationError
from source.exceptions.notFoundException import EdgeNotFoundError, NodeNotFoundError

EXPECTED = {("a", "b"), ("b", "c"), ("c", "a"), ("b", "a")}


@pytest.fixture
def g(build):
    # a->b, b->c, c->a и встречное b->a; d изолирована
    return build("abcd", [("a", "b", 1), ("b", "c", 2), ("c", "a", 3), ("b", "a", 4)])


# ============================ значения ============================

def test_yields_all_edges_once(g):
    items = list(g.edges())
    assert set(items) == EXPECTED
    assert len(items) == len(EXPECTED)


def test_elements_are_pairs(g):
    for e in g.edges():
        assert isinstance(e, tuple)
        assert len(e) == 2


def test_direction_preserved(g):
    items = set(g.edges())
    assert ("a", "b") in items and ("b", "a") in items      # встречные рёбра — разные
    assert ("a", "c") not in items
    assert ("c", "b") not in items


def test_weight_is_not_part_of_element(g):
    assert all(len(e) == 2 for e in g.edges())


def test_every_yielded_edge_exists(g):
    for u, v in g.edges():
        assert g.has_edge(e_from=u, e_to=v) is True


def test_every_existing_edge_is_yielded(g):
    yielded = set(g.edges())
    for u in "abcd":
        for v in "abcd":
            assert g.has_edge(e_from=u, e_to=v) is ((u, v) in yielded)


def test_endpoints_are_nodes(g):
    for u, v in g.edges():
        assert g.has_node(u) and g.has_node(v)


def test_count_matches_edges_count(g):
    assert len(list(g.edges())) == g.edges_count


def test_empty_graph_yields_nothing(build):
    assert list(build().edges()) == []


def test_nodes_without_edges_yield_nothing(build):
    assert list(build("abc").edges()) == []


def test_edge_iteration_ignores_isolated_nodes(g):
    assert all("d" not in e for e in g.edges())


@pytest.mark.parametrize("n", [0, 1, 2, 5, 20])
def test_complete_graph(build, n):
    g = build(range(n), [(a, b) for a in range(n) for b in range(n) if a != b])
    items = list(g.edges())
    assert len(items) == n * (n - 1) == g.edges_count
    assert len(set(items)) == len(items)


def test_chain_graph(build):
    g = build(range(6), [(i, i + 1) for i in range(5)])
    assert set(g.edges()) == {(i, i + 1) for i in range(5)}


def test_star_graph(build):
    g = build(range(6), [(0, i) for i in range(1, 6)])
    assert set(g.edges()) == {(0, i) for i in range(1, 6)}


def test_reflects_deleted_edge(g):
    g.delete_edge("b", "a")
    assert set(g.edges()) == EXPECTED - {("b", "a")}


def test_reflects_deleted_node(g):
    g.delete_node("c")      # уходят b->c и c->a
    assert set(g.edges()) == {("a", "b"), ("b", "a")}


def test_reflects_added_edge(g):
    g.create_edge("a", "d", 9)
    assert set(g.edges()) == EXPECTED | {("a", "d")}


# ============================ протокол итератора ============================

def test_iterator_protocol(g):
    it = g.edges()
    assert iter(it) is it
    assert hasattr(it, "__next__")


def test_exhausted_iterator_keeps_raising_stop_iteration(g):
    it = g.edges()
    list(it)
    for _ in range(3):
        with pytest.raises(StopIteration):
            next(it)


def test_iterator_is_one_shot(g):
    it = g.edges()
    list(it)
    assert list(it) == []


def test_next_with_default(g):
    it = g.edges()
    list(it)
    assert next(it, None) is None


def test_empty_graph_next_raises_stop_iteration(build):
    with pytest.raises(StopIteration):
        next(build("ab").edges())


def test_new_iterator_each_call(g):
    assert list(g.edges()) == list(g.edges())


def test_independent_iterators(g):
    it1, it2 = g.edges(), g.edges()
    first = next(it1)
    next(it1)
    assert next(it2) == first


def test_interleaved_iterators(g):
    it1, it2 = g.edges(), g.edges()
    r1, r2 = [], []
    for _ in range(4):
        r1.append(next(it1))
        r2.append(next(it2))
    assert r1 == r2 and set(r1) == EXPECTED


def test_nested_iteration(g):
    pairs = [(e1, e2) for e1 in g.edges() for e2 in g.edges()]
    assert len(pairs) == 16


def test_iteration_over_nodes_and_edges_simultaneously(g):
    seen = 0
    for v in g.nodes():
        for e in g.edges():
            seen += 1
    assert seen == 4 * 4


def test_works_with_itertools(g):
    assert len(list(itertools.islice(g.edges(), 2))) == 2
    assert set(itertools.chain(g.edges())) == EXPECTED


def test_works_with_builtins(g):
    assert sorted(g.edges()) == sorted(EXPECTED)
    assert ("a", "b") in g.edges()
    assert ("a", "c") not in g.edges()
    assert {u for u, _ in g.edges()} == {"a", "b", "c"}
    assert all(len(e) == 2 for e in g.edges())
    assert any(e == ("c", "a") for e in g.edges())


def test_partial_consumption_then_rest(g):
    it = g.edges()
    head = [next(it), next(it)]
    assert set(head + list(it)) == EXPECTED


# ============================ неизменность графа ============================

def test_full_iteration_does_not_change_graph(g, fingerprint):
    before = fingerprint(g, "abcdz")
    list(g.edges())
    assert fingerprint(g, "abcdz") == before


def test_partial_iteration_does_not_change_graph(g, fingerprint):
    before = fingerprint(g, "abcdz")
    next(g.edges())
    assert fingerprint(g, "abcdz") == before


def test_nested_iteration_does_not_change_graph(g, fingerprint):
    before = fingerprint(g, "abcdz")
    for _ in g.edges():
        for _ in g.edges():
            pass
    assert fingerprint(g, "abcdz") == before


def test_yielded_tuples_are_immutable(g):
    e = next(g.edges())
    with pytest.raises(TypeError):
        e[0] = "zzz"


def test_changing_yielded_list_does_not_affect_graph(g):
    items = list(g.edges())
    items.clear()
    assert g.edges_count == 4
    assert set(g.edges()) == EXPECTED


def test_masses_unchanged_after_iteration(build):
    g = build("ab", [("a", "b", 7)])
    list(g.edges())
    g.delete_edge("a", "b")          # ребро цело и удаляется штатно
    assert g.edges_count == 0


def test_abandoned_iterator_does_not_block_graph(g):
    it = g.edges()
    next(it)
    del it
    g.create_edge("a", "d", 1)
    assert g.edges_count == 5


# ============================ исключения графа и итератор ============================

def test_delete_all_yielded_edges(g):
    for e in list(g.edges()):             # сначала снимок, потом удаление
        g.delete_edge(*e)
    assert g.edges_count == 0
    assert g.nodes_count == 4
    assert list(g.edges()) == []


@pytest.mark.parametrize("edge", sorted(EXPECTED))
def test_double_delete_of_yielded_edge_raises(g, edge):
    assert edge in list(g.edges())
    g.delete_edge(*edge)
    with pytest.raises(EdgeNotFoundError):
        g.delete_edge(*edge)
    assert edge not in list(g.edges())


def test_reverse_of_one_way_edge_is_missing(g):
    assert ("b", "c") in set(g.edges())
    assert ("c", "b") not in set(g.edges())
    with pytest.raises(EdgeNotFoundError):
        g.delete_edge("c", "b")


def test_edge_iteration_after_node_deleted_and_edge_delete_raises(g):
    g.delete_node("a")
    assert all("a" not in e for e in g.edges())
    # РЕШЕНИЕ: допустимо любое из двух «не найдено»; зафиксируй своё
    with pytest.raises((EdgeNotFoundError, NodeNotFoundError)):
        g.delete_edge("a", "b")


def test_create_edge_with_missing_node_raises_and_edges_unchanged(g):
    with pytest.raises(NodeNotFoundError):
        g.create_edge("a", "zzz", 1)
    with pytest.raises(NodeNotFoundError):
        g.create_edge("zzz", "a", 1)
    assert set(g.edges()) == EXPECTED


def test_create_edge_with_bad_mass_raises_and_edges_unchanged(g):
    with pytest.raises(BadTypeError):
        g.create_edge("a", "d", "heavy")
    assert set(g.edges()) == EXPECTED


def test_duplicate_node_does_not_change_edges(g):
    with pytest.raises(NodeDuplicationError):
        g.create_node("a")
    assert set(g.edges()) == EXPECTED


def test_delete_missing_node_does_not_change_edges(g):
    with pytest.raises(NodeNotFoundError):
        g.delete_node("zzz")
    assert set(g.edges()) == EXPECTED


def test_delete_node_removes_yielded_edges_and_second_delete_raises(g):
    g.delete_node("b")
    assert set(g.edges()) == {("c", "a")}
    with pytest.raises(NodeNotFoundError):
        g.delete_node("b")
    assert set(g.edges()) == {("c", "a")}


# ============================ изменение графа во время итерации ============================
# РЕШЕНИЕ: любое структурное изменение инвалидирует итератор -> RuntimeError на следующем next().

@pytest.mark.parametrize("mutation", [
    lambda g: g.create_edge("a", "d", 1),
    lambda g: g.delete_edge("c", "a"),
    lambda g: g.create_node("z"),
    lambda g: g.delete_node("d"),
    lambda g: g.delete_node("a"),
], ids=["create_edge", "delete_edge", "create_node", "delete_isolated", "delete_with_edges"])
def test_change_during_iteration_raises(g, mutation):
    it = g.edges()
    next(it)
    mutation(g)
    with pytest.raises(RuntimeError):
        next(it)


def test_change_between_creation_and_first_next_raises(g):
    it = g.edges()
    g.create_edge("a", "d", 1)
    with pytest.raises(RuntimeError):
        next(it)


def test_new_iterator_works_after_invalidated_one(g):
    it = g.edges()
    next(it)
    g.create_edge("a", "d", 1)
    with pytest.raises(RuntimeError):
        next(it)
    assert set(g.edges()) == EXPECTED | {("a", "d")}


def test_invalidated_iterator_keeps_raising(g):
    it = g.edges()
    next(it)
    g.create_node("z")
    for _ in range(2):
        with pytest.raises(RuntimeError):
            next(it)


@pytest.mark.parametrize("failing", [
    lambda g: g.create_edge("a", "missing", 1),
    lambda g: g.create_edge("missing", "a", 1),
    lambda g: g.create_edge("a", "d", "heavy"),
    lambda g: g.delete_edge("a", "c"),
    lambda g: g.delete_node("missing"),
    lambda g: g.create_node("a"),
    lambda g: g.create_node([1]),
], ids=["to_missing", "from_missing", "bad_mass", "missing_edge",
        "missing_node", "duplicate_node", "unhashable"])
def test_failed_operation_does_not_invalidate_iterator(g, failing):
    it = g.edges()
    first = next(it)
    with pytest.raises((NodeNotFoundError, EdgeNotFoundError, NodeDuplicationError, BadTypeError)):
        failing(g)
    assert set([first] + list(it)) == EXPECTED


# ============================ случайные графы против эталона ============================

def model_edges(model):
    return {(a, b) for a in model for b in model[a]}


@pytest.mark.parametrize("seed", range(10))
def test_random_graph_matches_model(random_graph, seed):
    g, model = random_graph(seed)
    items = list(g.edges())
    assert set(items) == model_edges(model)
    assert len(items) == len(set(items)) == g.edges_count


@pytest.mark.parametrize("seed", range(10))
def test_random_edge_deletions_match_model(random_graph, seed):
    import random
    g, model = random_graph(seed)
    rng = random.Random(seed)
    edges = sorted(model_edges(model))
    for a, b in rng.sample(edges, min(5, len(edges))):
        g.delete_edge(a, b)
        del model[a][b]
        assert set(g.edges()) == model_edges(model)
        assert len(list(g.edges())) == g.edges_count


@pytest.mark.parametrize("seed", range(10))
def test_random_node_deletions_match_model(random_graph, seed):
    import random
    g, model = random_graph(seed)
    rng = random.Random(seed)
    for v in rng.sample(sorted(model), 4):
        g.delete_node(v)
        del model[v]
        for out in model.values():
            out.pop(v, None)
        assert set(g.edges()) == model_edges(model)
        assert len(list(g.edges())) == g.edges_count
