# $Collection: Stack$
# $DEF
from typing import Generic, List, TypeVar

VT = TypeVar("VT")


class Stack(Generic[VT]):
    _stack: List[VT]
    _n_op: int

    def __init__(self) -> None:
        self._stack = []
        self._n_op = 0

    def push(self, el: VT) -> None:  # $CX_DEF: 2$
        self._stack.insert(0, el)  # 2

        self._n_op += 2

    def pop(self) -> VT:  # $CX_DEF: 5$
        assert not self.empty, "Can't pop from empty queue!"  # 2

        el = self._stack.pop(0)  #  3

        self._n_op += 5

        return el

    @property
    def empty(self) -> bool:  # $CX_DEF: 2$
        return len(self._stack) == 0

    @property
    def n_op(self) -> int:
        return self._n_op

    @property
    def size(self) -> int:  # 1
        return len(self._stack)

    @property
    def top(self) -> VT:  # 3
        assert not self.empty, "Can't get top from empty stack!"  # 2

        return self._stack[0]


def print_stack(stack: Stack[VT]) -> None:
    buffer = Stack[VT]()

    elements = []
    for _ in range(stack.size):
        el = stack.pop()
        elements.append(el)
        buffer.push(el)

    print("Stack[" + ", ".join(map(str, elements)) + "]")

    for _ in range(buffer.size):
        stack.push(buffer.pop())


def seek(stack: Stack[VT], pos: int) -> VT:  # $CX_DEF: 14*n + 11$
    assert pos <= stack.size and pos >= 0, "Invalid position!"  # 5

    buffer = Stack[VT]()  # 2

    for _ in range(pos):  # n * (
        buffer.push(stack.pop())  # 7
    # ) = 7n

    el = stack.top  # 5

    for _ in range(pos):  # n * (
        stack.push(buffer.pop())  # 7
    # ) = 7n

    stack._n_op += buffer.n_op

    return el


def push_by_pos(stack: Stack[VT], el: VT, pos: int) -> None:  # $CX_DEF: 14*n + 9$
    assert pos <= stack.size and pos >= 0, "Invalid position!"  # 5

    buffer = Stack[VT]()  # 2

    for _ in range(pos):  # n * (
        buffer.push(stack.pop())  # 7
    # ) = 7n

    stack.push(el)  # 2

    for _ in range(pos):  # n * (
        stack.push(buffer.pop())  # 7
    # ) = 7n

    stack._n_op += buffer.n_op


def pop_by_pos(stack: Stack[VT], pos: int) -> VT:  # $CX_DEF: 14*n + 12$
    assert pos <= stack.size and pos >= 0, "Invalid position!"  # 5

    buffer = Stack[VT]()  # 2

    for _ in range(pos):  # n * (
        buffer.push(stack.pop())  # 7
    # ) = 7n

    el = stack.pop()  # 5

    for _ in range(pos):  # n * (
        stack.push(buffer.pop())  # 7
    # ) = 7n

    stack._n_op += buffer.n_op

    return el


def push_front(stack: Stack[VT], el: VT) -> None:  # $CX_DEF: 2$
    stack.push(el)  # 2


def push_back(stack: Stack[VT], el: VT) -> None:  # $CX_DEF: 14*n + 4$
    buffer = Stack[VT]()  # 2

    while not stack.empty:  # n * (
        buffer.push(stack.pop())  # 7
    # ) = 7n

    stack.push(el)  # 2

    while not buffer.empty:  # n * (
        stack.push(buffer.pop())  # 7
    # ) = 7n


def pop_front(stack: Stack[VT]) -> VT:  # $CX_DEF: 5$
    return stack.pop()  # 5


def pop_back(stack: Stack[VT]) -> VT:  # $CX_DEF: 14*n + 7$
    buffer = Stack[VT]()  # 2

    while not stack.empty:  # n * (
        buffer.push(stack.pop())  # 7
    # ) = 7n

    el = buffer.pop()  # 5

    while not buffer.empty:  # n * (
        stack.push(buffer.pop())  # 7
    # ) = 7n

    return el


def swap(stack: Stack[VT], pos1: int, pos2: int) -> None:  # $CX_DEF: 56*n + 42$
    temp = pop_by_pos(stack, pos1)  #  14n + 12
    push_by_pos(stack, pop_by_pos(stack, pos2 - 1), pos1)  # 28n + 21
    push_by_pos(stack, temp, pos2)  # 14n + 9


def slice_(stack: Stack[VT], l: int = 0, r: int = -1) -> Stack[VT]:  # CX_DEF: 16*n + 27$
    slice_stack = Stack[VT]()  # 2
    buffer = Stack[VT]()  # 2

    if r == -1:  # 1
        r = stack.size - 1  # 3

    for _ in range(r + 1):  # (n + 1) * (
        buffer.push(stack.pop())  # 7
    # ) = 7n + 7

    for _ in range(r - l + 1):  # (n // 2 + 1) * (
        slice_stack.push(buffer.top)  # 5
        stack.push(buffer.pop())  # 7
    # ) = 5n + 10

    while not buffer.empty:  # n // 2 * (
        stack.push(buffer.pop())  # 7
    # ) = 4n

    return slice_stack


# $ENDEF
from random import randint  # ignore: E402

import pytest  # ignore: E402

Collection = Stack[int]


@pytest.fixture
def collection() -> Collection:
    return Collection()


@pytest.fixture
def data(collection: Collection) -> List:
    data = [randint(-100, 100) for _ in range(20)]
    for el in data:
        push_back(collection, el)

    return data


def test_seek(data: List, collection: Collection):
    for i, el in enumerate(data):
        assert seek(collection, i) == el


def test_push_by_pos(data: List, collection: Collection):
    data.insert(2, 20)
    push_by_pos(collection, 20, 2)

    for i, el in enumerate(data):
        assert seek(collection, i) == el


def test_pop_by_pos(data: List, collection: Collection):
    data.pop(2)
    pop_by_pos(collection, 2)

    for i, el in enumerate(data):
        assert seek(collection, i) == el


def test_push_front(data: List, collection: Collection):
    data.insert(0, 20)
    push_front(collection, 20)

    for i, el in enumerate(data):
        assert seek(collection, i) == el


def test_push_back(data: List, collection: Collection):
    data.append(20)
    push_back(collection, 20)

    for i, el in enumerate(data):
        assert seek(collection, i) == el


def test_pop_front(data: List, collection: Collection):
    d_el = data.pop(0)
    c_el = pop_front(collection)

    assert d_el == c_el

    for i, el in enumerate(data):
        assert seek(collection, i) == el


def test_pop_back(data: List, collection: Collection):
    d_el = data.pop()
    c_el = pop_back(collection)

    assert d_el == c_el

    for i, el in enumerate(data):
        assert seek(collection, i) == el


def test_swap(data: List, collection: Collection):
    data[2], data[5] = data[5], data[2]
    swap(collection, 2, 5)

    for i, el in enumerate(data):
        assert seek(collection, i) == el


def test_slice(data: List, collection: Collection):
    slice = data[5:16]
    slice_stack = slice_(collection, 5, 15)

    for i, el in enumerate(slice):
        assert seek(slice_stack, i) == el

    for i, el in enumerate(data):
        assert seek(collection, i) == el


def test_empty(collection: Collection):
    while not collection.empty:
        collection.pop()

    assert collection.size == 0
