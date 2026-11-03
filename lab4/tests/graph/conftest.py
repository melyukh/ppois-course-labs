import random

import pytest

from source.graph.oGraphAdjList import OGraphAdjacencyList


@pytest.fixture
def build():
    """build(nodes, edges) -> граф; edge = (from, to) или (from, to, mass)."""
    def _build(nodes=(), edges=()):
        g = OGraphAdjacencyList()
        for v in nodes:
            g.create_node(v)
        for e in edges:
            g.create_edge(e[0], e[1], e[2] if len(e) > 2 else 1)
        return g
    return _build


@pytest.fixture
def random_graph(build):
    """random_graph(seed, n, p) -> (граф, эталонная модель {from: {to: mass}}); без петель."""
    def _make(seed, n=12, p=0.25):
        rng = random.Random(seed)
        nodes = list(range(n))
        edges = [(a, b, rng.randrange(1, 10))
                 for a in nodes for b in nodes if a != b and rng.random() < p]
        model = {a: {} for a in nodes}
        for a, b, w in edges:
            model[a][b] = w
        return build(nodes, edges), model
    return _make


@pytest.fixture
def fingerprint():
    """Слепок состояния графа через публичные методы, не через тестируемые итераторы."""
    def _fp(g, universe):
        present = [v for v in universe if g.has_node(v)]
        return (
            g.nodes_count,
            g.edges_count,
            tuple(present),
            tuple((a, b) for a in universe for b in universe if g.has_edge(e_from=a, e_to=b)),
            tuple(tuple(sorted(g.node_power(v).items())) for v in present),
        )
    return _fp
