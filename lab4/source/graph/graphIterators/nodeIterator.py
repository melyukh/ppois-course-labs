from typing import List, TypeVar
from collections.abc import Hashable, Iterator

T = TypeVar('HashableT', bound=Hashable)

class NodeIterator(Iterator[T]):
    def __init__(self, graph) -> None:
        self.graph = graph
        self.version: int = graph.version
        self.keys: List[T] = list(graph.data.keys())
        self.current_position = -1

    def check_version(self) -> None:
        if self.graph.version != self.version:
            raise RuntimeError("Граф был изменён во время итерации")

    def __next__(self) -> T:
        self.check_version()
        try:
            self.current_position += 1
            return self.keys[self.current_position]
        except IndexError:
            raise StopIteration

    def __iter__(self) -> "NodeIterator":
        return self

    def prev(self) -> T:
        self.check_version()
        self.current_position -= 1
        if(self.current_position < 0):
            raise StopIteration
        return self.keys[self.current_position]