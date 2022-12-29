# $Collection: Queue$
# $DEF
from typing import Generic, List, Optional, TypeVar

VT = TypeVar("VT")


class Node(Generic[VT]):
    _value: VT
    next: Optional["Node[VT]"]

    def __init__(self, value: VT, next: Optional["Node[VT]"] = None):
        self._value = value
        self.next = next

    @property
    def value(self) -> VT:
        return self._value

    def __str__(self) -> str:
        return str(self._value)


class Queue(Generic[VT]):
    _head: Optional[Node[VT]]
    _tail: Optional[Node[VT]]
    _size: int
    _n_op: int

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0
        self._n_op = 0

    def push(self, value: VT):  # 7
        node = Node(value)  # 2

        if self.empty:  # 1
            self._head = node  # 1
            self._tail = node  # 1
        else:
            self._tail.next = node  # 2
            self._tail = node  # 1

        self._size += 1  # 1
        self._n_op += 7

    def pop(self) -> VT:  # 8
        assert not self.empty, "Can't pop from empty queue!"  # 2

        node = self._head  # 1
        self._head = node.next  # 2

        if self._head is None:  # 1
            self._tail = None  # 1

        self._size -= 1  # 1
        self._n_op += 8

        return node.value

    @property
    def empty(self) -> bool:  # 2
        return self._size == 0

    @property
    def head(self) -> VT:  # 4
        assert not self.empty, "Can't get tail from empty dequeue!"  # 2

        self._n_op += 4

        return self._head.value

    @property
    def tail(self) -> VT:  # 4
        assert not self.empty, "Can't get tail from empty dequeue!"  # 2

        self._n_op += 4

        return self._tail.value

    @property
    def size(self) -> int:  # 1
        return self._size

    @property
    def n_op(self) -> int:
        return self._n_op


def print_queue(queue: Queue[VT]):
    elements = []
    for _ in range(queue.size):
        el = queue.pop()
        elements.append(el)
        queue.push(el)

    print("Queue[" + ", ".join(map(str, elements)) + "]")


def rotate(queue: Queue[VT]) -> None:  # 15
    queue.push(queue.pop())


def seek(queue: Queue[VT], pos: int) -> VT:  # 30n + 9
    assert pos <= queue.size and pos >= 0, "Invalid position!"  # 5

    for _ in range(pos):  # n * (
        rotate(queue)  # 15
    # ) = 15n

    el = queue.head  # 4

    for _ in range(queue.size - pos):  # n * (
        rotate(queue)  # 15
    # ) = 15n

    return el


def pop_by_pos(queue: Queue[VT], pos: int) -> VT:  # 30n + 13
    assert pos <= queue.size and pos >= 0, "Invalid position!"  # 5

    for _ in range(pos):  # n * (
        rotate(queue)  # 15
    # ) = 15n

    el = queue.pop()  # 8

    for _ in range(queue.size - pos):  # n * (
        rotate(queue)  # 15
    # ) = 15n

    return el


def push_by_pos(queue: Queue[VT], el: VT, pos: int) -> None:  # 30n + 14
    assert pos <= queue.size and pos >= 0, "Invalid position!"  # 5

    if pos >= queue.size:  # 2
        queue.push(el)  # 7
        return

    for _ in range(pos):  # n * (
        rotate(queue)  # 15
    # ) = 15n

    queue.push(el)  # 7

    for _ in range(queue.size - pos - 1):  # n * (
        rotate(queue)  # 15
    # ) = 15n


def push_back(queue: Queue[VT], el: VT) -> None:  # 7
    queue.push(el)  # 7


def push_front(queue: Queue[VT], el: VT) -> None:  # 15n + 7
    queue.push(el)  # 7
    for _ in range(queue.size - 1):  # n * (
        rotate(queue)  # 15
    # ) = 15n


def pop_back(queue: Queue[VT]) -> VT:  # 15n + 8
    for _ in range(queue.size - 1):  # n * (
        rotate(queue)  # 15
    # ) = 15n
    return queue.pop()  # 8


def pop_front(queue: Queue[VT]) -> VT:  # 8
    return queue.pop()  # 8


def swap(queue: Queue, pos1: int, pos2: int):  # 112n + 28
    temp = pop_by_pos(queue, pos1)  # 28n + 7
    push_by_pos(queue, pop_by_pos(queue, pos2 - 1), pos1)  # 56n + 14
    push_by_pos(queue, temp, pos2)  # 28n + 7


def slice_(queue: Queue[VT], l: int = 0, r: int = -1) -> Queue[VT]:  # 49n + 6
    buffer = Queue[VT]()  # 2

    if r == -1:  # 1
        r = queue.size - 1  # 3

    for _ in range(l):  # n * (
        rotate(queue)  # 14
    # ) = 14n

    for _ in range(r - l + 1):  # n * (
        el = queue.pop()  #  7

        buffer.push(el)  # 7

        queue.push(el)  # 7
    # ) = 21n

    for _ in range(queue.size - r - 1):  # n * (
        rotate(queue)  # 14
    # ) = 14n

    return buffer


# $ENDEF
from random import randint  # ignore: E402

import pytest  # ignore: E402

Collection = Queue[int]


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
