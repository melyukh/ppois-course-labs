from typing import Iterable, TypeVar, Callable, Any, MutableSequence, List

from source.protocols.comparable import Comparable
from source.protocols.integerMapped import IntegerMapped

from source.exceptions.badTypeException import BadTypeError

#жэнэрыки
T = TypeVar('T')
ComparableT = TypeVar('ComparableT', bound=Comparable)
IntegerMappedT = TypeVar('IntegerMappedT', bound=IntegerMapped)


#сортировка выбором
def selection_sort(items: Iterable[ComparableT], *,
                   key: Callable[[ComparableT], Any] | None = None, 
                   reversed_sort: bool = False) -> List[ComparableT]:
    if key is not None and not isinstance(key, Callable):
        raise BadTypeError("""Переданный key не  Callable, 
                            при попытке вычислить ключ сортировки возникнет ошибкa\n""")
    
    try:
        l_items = list(items)
    except TypeError:
        raise BadTypeError("""Передана неитерабельная колллекция: переданный тип данных должен соблюдать
                            контракт Iterable, т.е. реализовывать __iter__\n""")

    l_items = l_items[::-1] if reversed_sort else l_items
    
    length: int = len(l_items)

    for i in range(length):
        current_minimum_item: ComparableT = l_items[i]
        current_minimum_index: int = i
        for j in range(i + 1, length):
            item = l_items[j] 
            keyed_minimum_item = key(current_minimum_item) if key is not None else current_minimum_item
            keyed_element = key(item) if key is not None else item

            try:
                if keyed_element < keyed_minimum_item:
                    current_minimum_index = j
                    current_minimum_item = item
            except TypeError:
                raise BadTypeError("""Ошибка сравнения: сравниваемые элементы
                                    не имеют реализации __lt__ для соответствующих типов, 
                                    не могут быть отсортированы относительно друг друга\n""")

        l_items.insert(i, l_items.pop(current_minimum_index))

    return l_items[::-1] if reversed_sort else l_items

def selection_sort_inplace(items: MutableSequence[ComparableT], *,
                   key: Callable[[ComparableT], Any] | None = None, 
                   reversed_sort: bool = False) -> None:
    for i, value in enumerate(selection_sort(items, key=key, reversed_sort=reversed_sort)):
        items[i] = value


#сортировка вставками
def insertion_sort(items: Iterable[ComparableT], *,
                   key: Callable[[ComparableT], Any] | None = None, 
                   reversed_sort: bool = False) -> List[ComparableT]:
    if key is not None and not isinstance(key, Callable):
        raise BadTypeError("""Переданный key не  Callable, 
                            при попытке вычислить ключ сортировки возникнет ошибкa\n""")
    
    try:
        l_items = list(items)
    except TypeError:
        raise BadTypeError("""Передана неитерабельная колллекция: переданный тип данных должен соблюдать
                            контракт Iterable, т.е. реализовывать __iter__\n""")

    l_items = l_items[::-1] if reversed_sort else l_items
    length: int  = len(l_items)

    # ключи только один раз считаем, а не пересчитываем каждый раз, меняем позиции в массиве при необходимости
    keys: List[Callable[[ComparableT], Any]] = [key(x) if key is not None else x for x in l_items] 

    for i in range(1, length):
        current_item: ComparableT = l_items[i]
        current_key: Callable[[ComparableT], Any] = keys[i]

        j = i - 1
        while(j >= 0 and keys[j] > current_key):
            l_items[j+1] = l_items[j]
            keys[j+1]  = keys[j]
            j = j - 1

        l_items[j+1] = current_item
        keys[j+1]  = current_key

    return l_items[::-1] if reversed_sort else l_items

def insertion_sort_inplace(items: MutableSequence[ComparableT], *,
                   key: Callable[[ComparableT], Any] | None = None, 
                   reversed_sort: bool = False) -> None:
    for i, value in enumerate(insertion_sort(items, key=key, reversed_sort=reversed_sort)):
        items[i] = value


#сортировка подсчетом: вместо ключа сортировки считается вхождение элемента в коллекцию
def counting_sort(items: Iterable[T], *,
                   key: Callable[[IntegerMappedT], Any] | None = None, 
                   reversed_sort: bool = False) -> List[IntegerMappedT]:
    if key is not None and not isinstance(key, Callable):
            raise BadTypeError("""Переданный key не  Callable, 
                                при попытке вычислить ключ сортировки возникнет ошибкa\n""")
    try:
        l_items = list(items)
    except TypeError:
        raise BadTypeError("""Передана неитерабельная колллекция: переданный тип данных должен соблюдать
                            контракт Iterable, т.е. реализовывать __iter__\n""")

    l_items = l_items[::-1] if reversed_sort else l_items
    keys: List[int] = [key(x) if key is not None else x for x in l_items]
    if not all([isinstance(k, int) for k in keys]): 
        raise BadTypeError("""Некоторые значения не маппятся в целочисленные ключи""")

    if len(l_items) == 0:
        return l_items

    low:  int = min(keys)
    high: int = max(keys)

    size: int = high - low + 1

    count = [0 for _ in range(size)]

    for i in range(len(l_items)):
        count[keys[i] - low] += 1

    for i in range(1, size):
        count[i] += count[i - 1]

    output = [None for _ in range(len(l_items))]
    for i in range(len(l_items) - 1, -1, -1):
        c = keys[i] - low
        count[c] -= 1
        output[count[c]] = l_items[i]

    return output[::-1] if reversed_sort else output


def counting_sort_inplace(items: MutableSequence[T], *,
                   key: Callable[[IntegerMappedT], Any] | None = None, 
                   reversed_sort: bool = False) -> None:
    for i, value in enumerate(counting_sort(items, key=key, reversed_sort=reversed_sort)):
        items[i] = value