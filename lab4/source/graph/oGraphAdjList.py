from typing import  Dict, TypeVar, Callable, Any
from collections.abc import Hashable
from functools import wraps

from source.exceptions.notFoundException import NodeNotFoundError, EdgeNotFoundError
from source.exceptions.badTypeException import BadTypeError
from source.exceptions.nodeDuplicationException import NodeDuplicationError

from source.graph.graphIterators.adjacentNodeIterator import AdjacentNodeIterator
from source.graph.graphIterators.nodeIterator import NodeIterator
from source.graph.graphIterators.reversedNodeIterator import ReversedNodeIterator
from source.graph.graphIterators.incidentEdgeIterator import IncidentEdgeIterator
from source.graph.graphIterators.edgeIterator import EdgeIterator

T = TypeVar('HashableT', bound=Hashable)

def is_hashable_type_got(func: Callable):
    """Обертка для функции, которая перед тем как вызвать функцию проверяет args на иммутабельность типов
    Args:
        func(Callable): оборачиваемая функция

    Raises:
        BadTypeError: выбрасывается когда есть хотя бы один неиммутабельный тип данных в наборе аргументов
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        try:
            for element in args:
                hash(element)
        except TypeError:
            raise BadTypeError(f"переданный объект {element} имеет тип {type(element)}, который не является хэшируемым")

        return func(*args, **kwargs)
    return wrapper


class OGraphAdjacencyList[T]:
    def __init__(self) -> None:
        self._adjacency: Dict[T, Dict[T, int]] = {}
        self._nodes_count: int = 0
        self._edges_count: int = 0
        self._version: int = 0


    #==========Методы для работы с графом (переопределение dunder-ов как для словаря)==========#
    def __getitem__(self, key: T) -> Dict[T, int]:
        try: 
            return self._adjacency[key]
        except KeyError:
            raise KeyError("Нет ноды с таким ключом")

    def __setitem__(self, key: T, value: Dict[T, int]) -> None:
        self._adjacency[key] = value
        self._version += 1

    def __contains__(self, item: T) -> bool:
        return item in self._adjacency 

    def __len__(self) -> int:
        return len(self._adjacency)


    #==========Проверка наличия==========#
    @is_hashable_type_got
    def has_node(self, value: T) -> bool:
        return value in self._adjacency

    @is_hashable_type_got
    def has_edge(self, *, e_from: T, e_to: T) -> bool:
        return e_to in self._adjacency.get(e_from, {})


    #==========Версия графа: отслеживает изменения для Runtime-обработки исключений, когда итератор пытается пройтись по изменившемуся графу==========#
    @property
    def version(self) -> int:
        return self._version

    #==========Пропы для количества элементов==========#
    @property
    def data(self) ->  Dict[T, Dict[T, int]]:
        return self._adjacency

    @property
    def nodes_count(self) -> int:
        return self._nodes_count

    @property
    def edges_count(self) -> int:
        return self._edges_count

    #==========Добавление и удаление==========#
    @is_hashable_type_got
    def create_node(self, value: T) -> None:
        if self.has_node(value):
            raise NodeDuplicationError(f"Нода c ключом {value} уже задана")

        self._adjacency[value] = {}
        self._nodes_count += 1
        self._version += 1
        

    @is_hashable_type_got
    def delete_node(self, value: T):
        deleted_node = self._adjacency.pop(value, None)

        if deleted_node is None:
            raise NodeNotFoundError("Нет такой ноды")

        self._edges_count -= len(deleted_node)

        for key in self._adjacency:
            if value in self._adjacency[key]:
                self._adjacency[key].pop(value)
                self._edges_count -= 1

        self._nodes_count -= 1
        self._version += 1

    @is_hashable_type_got
    def create_edge(self, e_from: T, e_to: T, mass: int = -1) -> None:
        if not self.has_node(e_from) or not self.has_node(e_to):
            raise NodeNotFoundError("Нет нод между которыми вы проводите ребро")
        if not isinstance(mass, int):
            raise BadTypeError("Переданное значение для веса узла не int")

        if e_to not in self._adjacency[e_from]:
            self._edges_count += 1

        self._adjacency[e_from][e_to] = mass
        self._version += 1
        

    @is_hashable_type_got
    def delete_edge(self, e_from: T, e_to: T) -> None:
        if not self.has_node(e_from) or not self.has_node(e_to):
            raise NodeNotFoundError("Нет такой ноды")
        if e_to not in self._adjacency[e_from]:
            raise EdgeNotFoundError("Нет такого ребра")

        del self._adjacency[e_from][e_to]
        self._edges_count -= 1
        self._version += 1


    #==========Мощность ноды и связи(второе хз че такое, not implemented)==========#
    @is_hashable_type_got
    def node_power(self, value: T) -> Dict[str, int]:
        if value not in self._adjacency:
            raise NodeNotFoundError("Не найдена переданная нода")
        return {
            "to": len(self._adjacency[value]),
            "from": sum(1 for node in self._adjacency.values() if value in node)
        }

    def edge_power(self):
        raise NotImplementedError

    @is_hashable_type_got
    def edge_mass(self, e_from: T, e_to: T) -> int:
        if not self.has_node(e_from) or not self.has_node(e_to):
            raise NodeNotFoundError("Нет такой ноды")
        if e_to not in self._adjacency[e_from]:
            raise EdgeNotFoundError("Нет такого ребра")
        return self._adjacency[e_from][e_to]


    #==========Методы для создания итераторов==========#
    def __iter__(self):
        return NodeIterator(self)

    def __reversed__(self):
        return ReversedNodeIterator(self)

    def nodes(self):
        return NodeIterator(self)

    def edges(self):
        return EdgeIterator(self)

    @is_hashable_type_got
    def incident_edges(self, node: T):
        if not self.has_node(node):
            raise NodeNotFoundError("Нет такой ноды")
        return IncidentEdgeIterator(self, node)

    @is_hashable_type_got
    def adjacent_nodes(self, node: T):
        if not self.has_node(node):
            raise NodeNotFoundError("Нет такой ноды")
        return AdjacentNodeIterator(self, node)