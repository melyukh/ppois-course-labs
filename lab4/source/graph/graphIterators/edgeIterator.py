from typing import List, Tuple, TypeVar
from collections.abc import Hashable, Iterator

T = TypeVar("HashableT", bound=Hashable)

class EdgeIterator(Iterator[T]):
    def __init__(self, graph) -> None:
        self.graph = graph
        self.version: int = graph.version
        self.edges: List[Tuple[T, T]] = [
            (source, target)
            for source, neighbors in graph.data.items()
            for target in neighbors
        ]
        self.current_position = -1

    def check_version(self) -> None:
        if self.graph.version != self.version:
            raise RuntimeError("Граф был изменён во время итерации")

    def __next__(self) -> Tuple[T, T]:
        self.check_version()
        try:
            self.current_position += 1
            return self.edges[self.current_position]
        except IndexError:
            raise StopIteration

    def __iter__(self) -> "EdgeIterator":
        return self

    def prev(self) -> Tuple[T, T]:
        self.check_version()
        self.current_position -= 1
        if self.current_position < 0:
            raise StopIteration
        return self.edges[self.current_position]