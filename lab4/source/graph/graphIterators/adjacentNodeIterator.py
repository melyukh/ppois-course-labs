from typing import List, TypeVar
from collections.abc import Hashable, Iterator

T = TypeVar('HashableT', bound=Hashable)

class AdjacentNodeIterator(Iterator[T]):
    def __init__(self, graph, node: T) -> None:
        self.graph = graph
        self.version: int = graph.version
        self.nodes: List[T] = list(graph.data[node].keys())
        self.current_position = -1

    def check_version(self) -> None:
        if self.graph.version != self.version:
            raise RuntimeError("Граф был изменён во время итерации")

    def __next__(self) -> T:
        self.check_version()
        self.current_position += 1
        try:
            return self.nodes[self.current_position]
        except IndexError:
            raise StopIteration

    def __iter__(self) -> "AdjacentNodeIterator":
        return self

    def prev(self) -> T:
        self.check_version()
        self.current_position -= 1
        if self.current_position < 0:
            raise StopIteration
        return self.nodes[self.current_position]