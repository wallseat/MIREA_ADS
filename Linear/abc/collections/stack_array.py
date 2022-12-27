# $Collection: Stack$
# $DEF$
from typing import Generic, List, TypeVar

VT = TypeVar("VT")


class Stack(Generic[VT]):
    _stack: List[VT]
    _array_size: int
    _size: int
    _n_op: int

    def __init__(self) -> None:
        self._stack = [0]
        self._array_size = 1

        self._n_op = 0
        self._size = 0

    def push(self, el: VT) -> None:  # 13
        if self._size == self._array_size:  # 3
            self._stack += [0] * self._array_size  # 3
            self._array_size *= 2  # 2

            self._n_op += 5

        self._stack[self.size] = el  # 3
        self._size += 1  # 2

        self._n_op += 8

    def pop(self) -> VT:  # 9
        if self.empty:  # 2
            raise Exception("Can't pop from empty stack!")

        el = self._stack[self._size - 1]  #  5
        self._size -= 1  # 2

        self._n_op += 9

        return el

    @property
    def empty(self) -> bool:  # 2
        return self._size == 0

    @property
    def n_op(self) -> int:
        return self._n_op

    @property
    def size(self) -> int:  # 1
        return self._size

    @property
    def top(self) -> VT:  # 1
        if self.empty:
            raise Exception("Can't get top from empty stack!")
        return self._stack[self._size - 1]


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


def seek(stack: Stack[VT], pos: int) -> VT:  # 44n + 4
    buffer = Stack[VT]()  # 2

    for _ in range(pos):  # n * (
        buffer.push(stack.pop())  # 22
    # ) = 22n

    el = stack.top  # 2

    for _ in range(pos):  # n * (
        stack.push(buffer.pop())  # 22
    # ) = 22n

    stack._n_op += buffer.n_op

    return el


def push_by_pos(stack: Stack[VT], el: VT, pos: int) -> None:  # 44n + 15
    buffer = Stack[VT]()  # 2

    for _ in range(pos):  # n * (
        buffer.push(stack.pop())  # 22
    # ) = 22n

    stack.push(el)  # 13

    for _ in range(pos):  # n * (
        stack.push(buffer.pop())  # 22
    # ) = 22n

    stack._n_op += buffer.n_op


def pop_by_pos(stack: Stack[VT], pos: int) -> VT:  # 44n + 11
    buffer = Stack[VT]()  # 2

    for _ in range(pos):  # n * (
        buffer.push(stack.pop())  # 22
    # )= 22n

    el = stack.pop()  # 9

    for _ in range(pos):  # n * (
        stack.push(buffer.pop())  # 22
    # ) = 22n

    stack._n_op += buffer.n_op

    return el


def push_front(stack: Stack[VT], el: VT) -> None:  # 13
    stack.push(el)  # 13


def push_back(stack: Stack[VT], el: VT) -> None:  # 46n + 13
    buffer = Stack[VT]()  # 2

    while not stack.empty:  # n * (
        buffer.push(stack.pop())  # 22
    # ) = 22n

    stack.push(el)  # 13

    while not buffer.empty:  # n * (
        stack.push(buffer.pop())  # 22
    # ) = 22n


def pop_front(stack: Stack[VT]) -> VT:  # 9
    return stack.pop()  # 9


def pop_back(stack: Stack[VT]) -> VT:  # 44n + 11
    buffer = Stack[VT]()  # 2

    while not stack.empty:  # n * (
        buffer.push(stack.pop())  # 22
    # ) = 22n

    el = buffer.pop()  # 9

    while not buffer.empty:  # n * (
        stack.push(buffer.pop())  # 22
    # ) = 22n

    return el


def swap(stack: Stack[VT], pos1: int, pos2: int) -> None:  # 176n + 52
    temp = pop_by_pos(stack, pos1)  #  44n + 11
    push_by_pos(stack, pop_by_pos(stack, pos2 - 1), pos1)  # 88n + 26
    push_by_pos(stack, temp, pos2)  # 44n + 15


def slice_(stack: Stack[VT], l: int = 0, r: int = -1) -> Stack[VT]:  # 51n + 66
    slice_stack = Stack[VT]()  # 2
    buffer = Stack[VT]()  # 2

    if r == -1:  # 1
        r = stack.size - 1  # 3

    for _ in range(r + 1):  # (n + 1) * (
        buffer.push(stack.pop())  # 22
    # ) = 22n + 22

    for _ in range(r - l + 1):  # (n // 2 + 1) * (
        slice_stack.push(buffer.top)  # 14
        stack.push(buffer.pop())  # 22
    # ) = 18n + 36

    while not buffer.empty:  # n // 2 * (
        stack.push(buffer.pop())  # 22
    # ) = 11n

    return slice_stack


# $ENDEF$
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
