"""Тесты сортировок: selection / insertion / counting, копирующие и inplace-версии.

Контракт, который проверяется (как у встроенного sorted):
  - sort(items, *, key=None, reversed_sort=False) -> новый list, исходная коллекция не меняется;
  - sort_inplace(items, *, key=None, reversed_sort=False) -> None, меняет items на месте;
  - reversed_sort эквивалентен sorted(..., reverse=True): равные по ключу элементы сохраняют
    исходный порядок;
  - counting_sort принимает только целочисленные ключи.
"""
import random
from collections import Counter, UserList
from dataclasses import dataclass, field
from functools import total_ordering

import pytest

from source.exceptions.badTypeException import BadTypeError
from source.sort.sort import (                                   
    selection_sort, insertion_sort, counting_sort,
    selection_sort_inplace, insertion_sort_inplace, counting_sort_inplace
)


#UNSTABLE_ALGORITHMS: если какая-то реализация неустойчивая (например, selection на swap), то тесты устойчивости для неё будут пропущены.
UNSTABLE_ALGORITHMS: set = set()

COMPARISON_SORTS = [selection_sort, insertion_sort]
ALL_SORTS = [*COMPARISON_SORTS, counting_sort]
INPLACE_PAIRS = [
    (selection_sort_inplace, selection_sort),
    (insertion_sort_inplace, insertion_sort),
    (counting_sort_inplace, counting_sort),
]
COMPARISON_INPLACE_PAIRS = INPLACE_PAIRS[:2]


def _ids(fns):
    return [f.__name__ for f in fns]


@pytest.fixture(params=ALL_SORTS, ids=_ids(ALL_SORTS))
def sort(request):
    """Любая копирующая сортировка (работает с int-ключами)."""
    return request.param


@pytest.fixture(params=COMPARISON_SORTS, ids=_ids(COMPARISON_SORTS))
def cmp_sort(request):
    """Только сравнительные сортировки (любые сравнимые типы)."""
    return request.param


@pytest.fixture(params=INPLACE_PAIRS, ids=[p[0].__name__ for p in INPLACE_PAIRS])
def pair(request):
    return request.param          # (inplace, copying)


@pytest.fixture(params=COMPARISON_INPLACE_PAIRS, ids=[p[0].__name__ for p in COMPARISON_INPLACE_PAIRS])
def cmp_pair(request):
    return request.param


@pytest.fixture
def stable_sort(sort):
    if sort in UNSTABLE_ALGORITHMS:
        pytest.skip(f"{sort.__name__} помечена как неустойчивая")
    return sort


# ------------------------------ вспомогательные типы ------------------------------

@dataclass(frozen=True)
class Item:
    key: int
    tag: str


@dataclass(frozen=True, order=True)
class Person:
    age: int
    name: str = field(compare=False)


@total_ordering
class OnlyLt:
    """Минимальный контракт Comparable: определены __eq__ и __lt__ (остальное достроит total_ordering)."""
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return f"OnlyLt({self.value})"


def random_ints(seed: int, n: int, spread: int) -> list[int]:
    rng = random.Random(seed)
    return [rng.randint(-spread, spread) for _ in range(n)]


def tagged(seed: int, n: int, distinct: int) -> list[Item]:
    rng = random.Random(seed)
    return [Item(rng.randrange(distinct), f"t{i}") for i in range(n)]


# =============================== базовая корректность ===============================

@pytest.mark.parametrize(
    "data",
    [
        [], [1], [2, 1], [1, 2], [3, 1, 2], [1, 2, 3, 4, 5], [5, 4, 3, 2, 1],
        [2, 2, 2, 2], [1, 2, 1, 2, 1], [-1, -5, 3, 0, -2], [0], [-1], [10**4, -10**4, 0],
        [7, 7, 3, 3, 9, 9, 1],
    ],
    ids=["empty", "single", "two_desc", "two_asc", "three", "sorted", "reversed",
         "all_equal", "alternating", "negatives", "zero", "minus_one", "extremes", "pairs"],
)
def test_matches_builtin_sorted(sort, data):
    assert sort(data) == sorted(data)


@pytest.mark.parametrize("n", [0, 1, 2, 3, 10, 50, 200])
@pytest.mark.parametrize("seed", range(5))
@pytest.mark.parametrize("spread", [3, 1000], ids=["many_duplicates", "mostly_unique"])
def test_random_data_matches_builtin_sorted(sort, n, seed, spread):
    data = random_ints(seed, n, spread)
    assert sort(data) == sorted(data)


@pytest.mark.parametrize("seed", range(5))
def test_result_is_permutation_of_input(sort, seed):
    data = random_ints(seed, 100, 10)
    assert Counter(sort(data)) == Counter(data)


@pytest.mark.parametrize("seed", range(5))
def test_result_is_ordered(sort, seed):
    result = sort(random_ints(seed, 100, 50))
    assert all(a <= b for a, b in zip(result, result[1:]))


def test_sorting_sorted_result_is_idempotent(sort):
    once = sort(random_ints(1, 80, 20))
    assert sort(once) == once


def test_returns_list(sort):
    assert type(sort([3, 1, 2])) is list


def test_empty_input_gives_empty_list(sort):
    assert sort([]) == []


def test_all_algorithms_agree(sort):
    data = random_ints(7, 150, 15)
    assert sort(data) == insertion_sort(data) == selection_sort(data) == counting_sort(data)


# =============================== входные коллекции ===============================

@pytest.mark.parametrize(
    "make",
    [tuple, iter, lambda d: (x for x in d), lambda d: list(d)],
    ids=["tuple", "iterator", "generator", "list"],
)
def test_accepts_any_iterable(sort, make):
    data = [5, 3, 9, 1, 3]
    assert sort(make(data)) == [1, 3, 3, 5, 9]


def test_accepts_range(sort):
    assert sort(range(5, 0, -1)) == [1, 2, 3, 4, 5]


def test_accepts_set_and_dict_keys(sort):
    assert sort({3, 1, 2}) == [1, 2, 3]
    assert sort({3: "a", 1: "b", 2: "c"}) == [1, 2, 3]


def test_generator_is_consumed_once_and_result_correct(sort):
    gen = (x for x in [4, 2, 3])
    assert sort(gen) == [2, 3, 4]
    assert list(gen) == []                          # коллекция исчерпана, повторно не нужна


def test_string_is_iterable_of_characters(cmp_sort):
    assert cmp_sort("hello") == ["e", "h", "l", "l", "o"]


# =============================== сравнимые типы (comparison) ===============================

@pytest.mark.parametrize(
    "data",
    [
        ["pear", "apple", "fig", "banana"],
        [3.5, -1.25, 2.0, 0.0],
        [(2, "b"), (1, "z"), (2, "a"), (1, "a")],
        [True, False, True],
        [3, 1.5, 2, 0.5],                           # int и float сравнимы между собой
        ["б", "а", "в", "ё"],
        [[2, 1], [1, 5], [1, 2], []],
    ],
    ids=["str", "float", "tuple", "bool", "int_float", "cyrillic", "lists"],
)
def test_comparison_sorts_with_various_types(cmp_sort, data):
    assert cmp_sort(data) == sorted(data)


def test_custom_class_with_only_lt(cmp_sort):
    data = [OnlyLt(v) for v in [5, 1, 4, 2, 3]]
    assert [x.value for x in cmp_sort(data)] == [1, 2, 3, 4, 5]


def test_dataclass_with_order(cmp_sort):
    people = [Person(30, "A"), Person(20, "B"), Person(25, "C")]
    assert [p.age for p in cmp_sort(people)] == [20, 25, 30]


def test_comparison_sorts_handle_huge_values(cmp_sort):
    # диапазон 2*10**9: для counting_sort это неприменимо (массив счётчиков), для сравнительных нормально
    data = [10**9, -10**9, 0, 10**18, -10**18]
    assert cmp_sort(data) == sorted(data)


def test_incomparable_types_raise(cmp_sort):
    with pytest.raises((TypeError, BadTypeError)):
        cmp_sort([1, "a", 2])


def test_none_among_numbers_raises(cmp_sort):
    with pytest.raises((TypeError, BadTypeError)):
        cmp_sort([3, None, 1])


# =============================== key ===============================

@pytest.mark.parametrize(
    "data, key",
    [
        (["ccc", "a", "bb", "dddd", ""], len),
        ([-3, 1, -2, 5, 0], abs),
        ([10, 25, 31, 42, 7], lambda x: x % 10),
        ([(1, 9), (2, 3), (0, 5)], lambda p: p[1]),
        ([5, 3, 8, 1], lambda x: -x),
        ([Person(30, "A"), Person(20, "B"), Person(25, "C")], lambda p: p.age),
    ],
    ids=["len", "abs", "mod10", "second_of_pair", "negated", "attribute"],
)
def test_key_matches_builtin(sort, data, key):
    assert sort(data, key=key) == sorted(data, key=key)


def test_key_none_equals_no_key(sort):
    data = [4, 1, 3, 2]
    assert sort(data, key=None) == sort(data)


def test_key_is_keyword_only(sort):
    with pytest.raises(TypeError):
        sort([2, 1], len)                           # type: ignore[misc]


def test_reversed_sort_is_keyword_only(sort):
    with pytest.raises(TypeError):
        sort([2, 1], None, True)                    # type: ignore[misc]


def test_key_does_not_change_elements(sort):
    data = ["bb", "a", "ccc"]
    result = sort(data, key=len)
    assert result == ["a", "bb", "ccc"]
    assert data == ["bb", "a", "ccc"]


def test_key_not_callable_raises_bad_type(sort):
    with pytest.raises(BadTypeError):
        sort([3, 1, 2], key="len")


@pytest.mark.parametrize("bad_key", [5, "abc", [1], {"k": 1}], ids=["int", "str", "list", "dict"])
def test_various_non_callable_keys(sort, bad_key):
    with pytest.raises(BadTypeError):
        sort([3, 1, 2], key=bad_key)


def test_key_exception_propagates(sort):
    def broken(_):
        raise ValueError("boom")

    with pytest.raises(ValueError, match="boom"):
        sort([3, 1, 2], key=broken)


def test_tuple_key_for_several_criteria(cmp_sort):
    data = [("b", 2), ("a", 2), ("c", 1), ("a", 1)]
    key = lambda p: (p[1], p[0])
    assert cmp_sort(data, key=key) == sorted(data, key=key)


# =============================== reversed_sort ===============================

@pytest.mark.parametrize("data", [[], [1], [3, 1, 2], [1, 2, 3], [3, 3, 1, 1, 2], [-2, 5, -2, 0]])
def test_reversed_sort_matches_builtin(sort, data):
    assert sort(data, reversed_sort=True) == sorted(data, reverse=True)


@pytest.mark.parametrize("seed", range(5))
def test_reversed_sort_random(sort, seed):
    data = random_ints(seed, 120, 10)
    assert sort(data, reversed_sort=True) == sorted(data, reverse=True)


def test_reversed_sort_is_reverse_for_unique_values(sort):
    data = random.Random(3).sample(range(1000), 60)
    assert sort(data, reversed_sort=True) == sort(data)[::-1]


def test_reversed_sort_false_is_default(sort):
    data = [3, 1, 2]
    assert sort(data, reversed_sort=False) == sort(data)


def test_reversed_sort_with_key(sort):
    data = [-3, 1, -2, 5, 0, 2]
    assert sort(data, key=abs, reversed_sort=True) == sorted(data, key=abs, reverse=True)


def test_reversed_sort_strings_by_len(cmp_sort):
    data = ["bb", "a", "ccc", "dd", "e"]
    assert cmp_sort(data, key=len, reversed_sort=True) == sorted(data, key=len, reverse=True)


def test_reversed_sort_does_not_change_input(sort):
    data = [3, 1, 2]
    sort(data, reversed_sort=True)
    assert data == [3, 1, 2]


# =============================== устойчивость ===============================

def test_stability_simple(stable_sort):
    data = [Item(1, "a"), Item(0, "b"), Item(1, "c"), Item(0, "d")]
    assert stable_sort(data, key=lambda i: i.key) == [Item(0, "b"), Item(0, "d"), Item(1, "a"), Item(1, "c")]


@pytest.mark.parametrize("seed", range(8))
@pytest.mark.parametrize("distinct", [1, 2, 5])
def test_stability_random(stable_sort, seed, distinct):
    data = tagged(seed, 60, distinct)
    key = lambda i: i.key
    assert stable_sort(data, key=key) == sorted(data, key=key)


@pytest.mark.parametrize("seed", range(8))
@pytest.mark.parametrize("distinct", [1, 2, 5])
def test_stability_with_reversed_sort(stable_sort, seed, distinct):
    # reversed_sort == sorted(reverse=True): равные ключи остаются в исходном порядке
    data = tagged(seed, 60, distinct)
    key = lambda i: i.key
    assert stable_sort(data, key=key, reversed_sort=True) == sorted(data, key=key, reverse=True)


def test_reversed_sort_does_not_just_reverse_the_result(stable_sort):
    data = [Item(1, "a"), Item(1, "b"), Item(2, "c")]
    result = stable_sort(data, key=lambda i: i.key, reversed_sort=True)
    assert result == [Item(2, "c"), Item(1, "a"), Item(1, "b")]       # a раньше b, как во входе


def test_multi_pass_sort_relies_on_stability(stable_sort):
    # сначала по второстепенному, потом по главному ключу
    data = [Item(2, "b"), Item(1, "b"), Item(2, "a"), Item(1, "a")]
    by_tag = stable_sort(data, key=lambda i: ord(i.tag))
    by_key = stable_sort(by_tag, key=lambda i: i.key)
    assert by_key == [Item(1, "a"), Item(1, "b"), Item(2, "a"), Item(2, "b")]


def test_equal_objects_keep_identity_and_order(stable_sort):
    a, b, c = Item(1, "x"), Item(1, "x"), Item(1, "x")          # равны, но три разных объекта
    result = stable_sort([a, b, c], key=lambda i: i.key)
    assert [id(x) for x in result] == [id(a), id(b), id(c)]


# =============================== исходные данные не меняются ===============================

def test_input_list_is_not_modified(sort):
    data = [5, 2, 9, 1]
    snapshot = list(data)
    sort(data)
    assert data == snapshot


def test_result_is_a_new_list(sort):
    data = [1, 2, 3]                                # уже отсортирован
    result = sort(data)
    assert result is not data
    result.append(99)
    assert data == [1, 2, 3]


def test_elements_are_same_objects_not_copies(cmp_sort):
    items = [[3], [1], [2]]
    result = cmp_sort(items)
    assert {id(x) for x in result} == {id(x) for x in items}


def test_input_tuple_stays_tuple(sort):
    data = (3, 1, 2)
    sort(data)
    assert data == (3, 1, 2)


def test_repeated_calls_give_same_result(sort):
    data = random_ints(11, 50, 10)
    assert sort(data) == sort(data) == sort(list(data))


# =============================== ошибки входа ===============================

@pytest.mark.parametrize("bad", [5, None, 3.14, object()], ids=["int", "none", "float", "object"])
def test_non_iterable_raises_bad_type(sort, bad):
    with pytest.raises(BadTypeError):
        sort(bad)


# =============================== counting_sort: специфика ===============================

def test_counting_without_key_on_ints():
    assert counting_sort([3, 1, 2]) == [1, 2, 3]


@pytest.mark.parametrize(
    "data",
    [[-5, -1, -3], [-2, 0, 2], [0, 0, 0], [100, 99, 101], [-10**6, 10**6]],
    ids=["all_negative", "around_zero", "zeros", "offset_range", "wide_range"],
)
def test_counting_ranges(data):
    assert counting_sort(data) == sorted(data)


def test_counting_sparse_range():
    data = [0, 10**6, 5, 10**6, 0]
    assert counting_sort(data) == sorted(data)


def test_counting_single_distinct_value():
    assert counting_sort([7] * 20) == [7] * 20


@pytest.mark.parametrize("seed", range(5))
def test_counting_large_input(seed):
    data = random_ints(seed, 3000, 100)
    assert counting_sort(data) == sorted(data)


def test_counting_with_object_key():
    people = [Person(30, "A"), Person(20, "B"), Person(25, "C"), Person(20, "D")]
    result = counting_sort(people, key=lambda p: p.age)
    assert [(p.age, p.name) for p in result] == [(20, "B"), (20, "D"), (25, "C"), (30, "A")]


@pytest.mark.parametrize(
    "keys",
    [[1.5, 2.5], ["a", "b"], [None, 1], [1, 2.0], [(1,), (2,)]],
    ids=["float", "str", "none", "int_and_float", "tuple"],
)
def test_counting_non_integer_keys_raise(keys):
    items = list(range(len(keys)))
    mapping = dict(zip(items, keys))
    with pytest.raises(BadTypeError):
        counting_sort(items, key=lambda i: mapping[i])


def test_counting_strings_without_key_raise():
    with pytest.raises(BadTypeError):
        counting_sort(["b", "a"])


def test_counting_floats_without_key_raise():
    with pytest.raises(BadTypeError):
        counting_sort([1.5, 0.5])


# =============================== inplace ===============================

def test_inplace_returns_none(pair):
    inplace, _ = pair
    data = [3, 1, 2]
    assert inplace(data) is None


def test_inplace_sorts_the_same_object(pair):
    inplace, _ = pair
    data = [3, 1, 2]
    same = data
    inplace(data)
    assert data is same
    assert data == [1, 2, 3]


@pytest.mark.parametrize("data", [[], [1], [2, 1], [3, 1, 2, 3, 1], [5, 4, 3, 2, 1], [-1, -3, 2, 0]])
def test_inplace_matches_builtin(pair, data):
    inplace, _ = pair
    inplace(data)
    assert data == sorted(data)


@pytest.mark.parametrize("seed", range(5))
def test_inplace_random_matches_copying_version(pair, seed):
    inplace, copying = pair
    data = random_ints(seed, 100, 10)
    expected = copying(data)
    inplace(data)
    assert data == expected


def test_inplace_with_key(pair):
    inplace, _ = pair
    data = [-3, 1, -2, 5, 0]
    inplace(data, key=abs)
    assert data == sorted([-3, 1, -2, 5, 0], key=abs)


def test_inplace_reversed_sort(pair):
    inplace, _ = pair
    data = [3, 1, 2, 3]
    inplace(data, reversed_sort=True)
    assert data == [3, 3, 2, 1]


@pytest.mark.parametrize("seed", range(5))
def test_inplace_stability_with_reversed_sort(pair, seed):
    inplace, copying = pair
    if copying in UNSTABLE_ALGORITHMS:
        pytest.skip("неустойчивая реализация")
    data = tagged(seed, 50, 3)
    expected = sorted(data, key=lambda i: i.key, reverse=True)
    inplace(data, key=lambda i: i.key, reversed_sort=True)
    assert data == expected


def test_inplace_keeps_length_and_elements(pair):
    inplace, _ = pair
    data = random_ints(2, 40, 5)
    before = Counter(data)
    inplace(data)
    assert len(data) == 40
    assert Counter(data) == before


def test_inplace_preserves_object_identity(cmp_pair):
    inplace, _ = cmp_pair
    items = [[3], [1], [2]]
    ids = {id(x) for x in items}
    inplace(items)
    assert {id(x) for x in items} == ids
    assert items == [[1], [2], [3]]


def test_inplace_other_references_see_the_change(pair):
    inplace, _ = pair
    data = [2, 1]
    alias = data
    inplace(data)
    assert alias == [1, 2]


def test_inplace_works_on_user_list(pair):
    inplace, _ = pair
    data = UserList([3, 1, 2])
    inplace(data)
    assert list(data) == [1, 2, 3]


def test_inplace_reflects_changes_for_nested_use(pair):
    inplace, _ = pair
    matrix = [[3, 1, 2], [9, 8, 7]]
    for row in matrix:
        inplace(row)
    assert matrix == [[1, 2, 3], [7, 8, 9]]


def test_inplace_key_not_callable_leaves_list_untouched(pair):
    inplace, _ = pair
    data = [3, 1, 2]
    with pytest.raises(BadTypeError):
        inplace(data, key="len")
    assert data == [3, 1, 2]


def test_inplace_on_tuple_raises(pair):
    inplace, _ = pair
    with pytest.raises((TypeError, BadTypeError)):
        inplace((3, 1, 2))


def test_inplace_non_iterable_raises(pair):
    inplace, _ = pair
    with pytest.raises((TypeError, BadTypeError)):
        inplace(5)


def test_inplace_counting_non_int_keys_leave_list_untouched():
    data = [1.5, 0.5]
    with pytest.raises(BadTypeError):
        counting_sort_inplace(data)
    assert data == [1.5, 0.5]