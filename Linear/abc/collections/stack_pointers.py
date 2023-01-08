# $Collection: Stack$
# $DEF
from numbers import Real
from typing import List, Optional


class Node:
    _value: Real
    next: Optional["Node"]

    def __init__(self, value: Real, next: Optional["Node"] = None):
        self._value = value
        self.next = next

    @property
    def value(self) -> Real:
        return self._value

    def __str__(self) -> str:
        return str(self._value)


class Stack:
    _top: Optional[Node]
    _size: int
    _n_op: int

    def __init__(self) -> None:
        self._top = None
        self._size = 0
        self._n_op = 0

    def push(self, value: Real) -> None:  # $CX_DEF: 14$
        node = Node(value)  # 2

        if self.empty:  # 2
            self._top = node  # 3
        else:
            node.next = self._top  # 3
            self._top = node  # 2

        self._size += 1  # 2
        self._n_op += 14

    def pop(self) -> Real:  # $CX_DEF: 10$
        assert not self.empty, "Can't pop from empty stack!"  # 2

        node = self._top  # 3
        self._top = node.next  # 3

        self._size -= 1  # 2
        self._n_op += 10

        return node.value

    @property
    def empty(self) -> bool:  # $CX_DEF: 2$
        return self._size == 0

    @property
    def top(self) -> Real:  # 4
        assert not self.empty, "Can't get top from empty stack!"  # 2

        return self._top.value

    @property
    def size(self) -> int:  # 1
        return self._size

    @property
    def n_op(self) -> int:
        return self._n_op


def print_stack(stack: Stack) -> None:
    buffer = Stack()

    elements = []
    for _ in range(stack.size):
        el = stack.pop()
        elements.append(el)
        buffer.push(el)

    print("Stack[" + ", ".join(map(str, elements)) + "]")

    for _ in range(buffer.size):
        stack.push(buffer.pop())


def seek(stack: Stack, pos: int) -> Real:  #  $CX_DEF: 48*n + 17$
    assert pos <= stack.size and pos >= 0, "Invalid position!"  # 5

    buffer = Stack()  # 2

    for _ in range(pos):  # n * (
        buffer.push(stack.pop())  # 24
    # ) = 24n

    el = stack.top  # 4

    for _ in range(pos):  # n * (
        stack.push(buffer.pop())  # 24
    # ) = 24n

    stack._n_op += buffer.n_op

    return el


def push_by_pos(stack: Stack, el: Real, pos: int) -> None:  # $CX_DEF: 48*n + 21$
    assert pos <= stack.size and pos >= 0, "Invalid position!"  # 5

    buffer = Stack()  # 2

    for _ in range(pos):  # n * (
        buffer.push(stack.pop())  # 24
    # ) = 24n

    stack.push(el)  # 14

    for _ in range(pos):  # n * (
        stack.push(buffer.pop())  # 24
    # ) = 24n

    stack._n_op += buffer.n_op


def pop_by_pos(stack: Stack, pos: int) -> Real:  # $CX_DEF: 48*n + 17$
    assert pos <= stack.size and pos >= 0, "Invalid position!"  # 5

    buffer = Stack()  # 2

    for _ in range(pos):  # n * (
        buffer.push(stack.pop())  # 24
    # ) = 24n

    el = stack.pop()  # 10

    for _ in range(pos):  # n * (
        stack.push(buffer.pop())  # 24
    # ) = 24n

    stack._n_op += buffer.n_op

    return el


def push_front(stack: Stack, el: Real) -> None:  # $CX_DEF: 14$
    stack.push(el)  # 14


def push_back(stack: Stack, el: Real) -> None:  # $CX_DEF: 48*n + 16$
    buffer = Stack()  # 2

    while not stack.empty:  # n * (
        buffer.push(stack.pop())  # 24
    # ) = 24n

    stack.push(el)  # 14

    while not buffer.empty:  # n * (
        stack.push(buffer.pop())  # 24
    # ) = 24n


def pop_front(stack: Stack) -> Real:  # $CX_DEF: 10$
    return stack.pop()  # 10


def pop_back(stack: Stack) -> Real:  # $CX_DEF: 48*n + 12$
    buffer = Stack()  # 2

    while not stack.empty:  # n * (
        buffer.push(stack.pop())  # 24
    # ) = 24n

    el = buffer.pop()  # 10

    while not buffer.empty:  # n * (
        stack.push(buffer.pop())  # 24
    # ) = 24n

    return el


def swap(stack: Stack, pos1: int, pos2: int) -> None:  # $CX_DEF: 192*n + 76$
    temp = pop_by_pos(stack, pos1)  #  48n + 17
    push_by_pos(stack, pop_by_pos(stack, pos2 - 1), pos1)  # 96n + 38
    push_by_pos(stack, temp, pos2)  # 48n + 21


def partition(stack: Stack, l: int = 0, r: int = -1) -> Stack:  # $CX_DEF: 56*n + 74$
    slice_stack = Stack()  # 2
    buffer = Stack()  # 2

    if r == -1:  # 1
        r = stack.size - 1  # 3

    for _ in range(r + 1):  # (n + 1) * (
        buffer.push(stack.pop())  # 24
    # ) = 24n + 24

    for _ in range(r - l + 1):  # (n // 2 + 1) * (
        slice_stack.push(buffer.top)  # 18
        stack.push(buffer.pop())  # 24
    # ) = 20n + 40

    while not buffer.empty:  # n // 2 * (
        stack.push(buffer.pop())  # 24
    # ) = 12n

    return slice_stack


# $ENDEF
from random import randint  # ignore: E402

import pytest  # ignore: E402

Collection = Stack


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
    slice_stack = partition(collection, 5, 15)

    for i, el in enumerate(slice):
        assert seek(slice_stack, i) == el

    for i, el in enumerate(data):
        assert seek(collection, i) == el


def test_empty(collection: Collection):
    while not collection.empty:
        collection.pop()

    assert collection.size == 0
