from typing import TypeVar
from collections.abc import Hashable
from source.graph.graphIterators.nodeIterator import NodeIterator

T = TypeVar('HashableT', bound=Hashable)

class ReversedNodeIterator(NodeIterator):
    def __init__(self, graph) -> None:
        super().__init__(graph)
        self.keys = self.keys[::-1]

    def __next__(self) -> T:
        return super().__next__()

    def __iter__(self) -> "ReversedNodeIterator":
        return super().__iter__()

    def prev(self) -> T:
        return super().prev()