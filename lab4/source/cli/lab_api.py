"""Единая точка импорта из кода лабы. Если у тебя другие пути или имена, правь только здесь."""
from source.sort.sort import (                                           # noqa: F401
    selection_sort, insertion_sort, counting_sort,
    selection_sort_inplace, insertion_sort_inplace, counting_sort_inplace,
)
from source.graph.oGraphAdjList import OGraphAdjacencyList              # noqa: F401
from source.exceptions.badTypeException import BadTypeError            # noqa: F401
from source.exceptions.notFoundException import NodeNotFoundError, EdgeNotFoundError   # noqa: F401
from source.exceptions.nodeDuplicationException import NodeDuplicationError            # noqa: F401

# Ошибки, которые CLI показывает пользователю как сообщение, а не падает.
HANDLED_ERRORS = (
    BadTypeError, NodeNotFoundError, EdgeNotFoundError, NodeDuplicationError,
    RuntimeError, ValueError, TypeError,
)
