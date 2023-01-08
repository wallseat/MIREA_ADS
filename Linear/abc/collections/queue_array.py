# $Collection: Queue$
# $DEF
from numbers import Real
from typing import List


class Queue:
    _queue: List
    _array_size: int

    _bias: int
    _size: int
    _n_op: int

    def __init__(self) -> None:
        self._queue = [0]
        self._array_size = 1

        self._size = 0
        self._n_op = 0
        self._bias = 0

    def push(self, value: Real) -> None:  # $CX_DEF: 13$
        if self._size == self._array_size:  # 3
            self._queue += [0] * self._array_size  # 3
            self._array_size *= 2  # 2

        self._queue[(self._size + self._bias) % self._array_size] = value  # 3
        self._size += 1  # 2

        self._n_op += 13

    def pop(self) -> Real:  # $CX_DEF: 14$
        assert not self.empty, "Can't pop from empty queue!"  # 2

        el = self._queue[self._bias]  # 4
        self._size -= 1  # 2
        self._bias = (self._bias + 1) % self._array_size  # 6

        self._n_op += 14

        return el

    @property
    def empty(self) -> bool:  # $CX_DEF: 2$
        return self._size == 0

    @property
    def size(self) -> int:  # 1
        return self._size

    @property
    def tail(self) -> Real:  # 10
        assert not self.empty, "Can't get head from empty dequeue!"  # 2

        self._n_op += 10

        return self._queue[(self._size - 1 + self._bias) % self._max_size]

    @property
    def head(self) -> Real:  # 5
        assert not self.empty, "Can't get tail from empty dequeue!"  # 2

        self._n_op += 5

        return self._queue[self._bias]

    @property
    def n_op(self) -> int:
        return self._n_op


def print_queue(queue: Queue):
    elements = []
    for _ in range(queue.size):
        el = queue.pop()
        elements.append(el)
        queue.push(el)

    print("Queue[" + ", ".join(map(str, elements)) + "]")


def rotate(queue: Queue) -> None:  # 27
    queue.push(queue.pop())  # 27


def seek(queue: Queue, pos: int) -> Real:  # $CX_DEF: 54*n + 32$
    assert pos <= queue.size and pos >= 0, "Invalid position!"  # 5

    for _ in range(pos):  # n * (
        rotate(queue)  # 27
    # ) = 27n

    el = queue.pop()  # 14
    queue.push(el)  # 13

    for _ in range(queue.size - pos - 1):  # n * (
        rotate(queue)  # 27
    # ) = 27n

    return el


def pop_by_pos(queue: Queue, pos: int) -> Real:  # $CX_DEF: 54*n + 19$
    assert pos <= queue.size and pos >= 0, "Invalid position!"  # 5

    for _ in range(pos):  # n * (
        rotate(queue)  # 27
    # ) = 27n

    el = queue.pop()  # 14

    for _ in range(queue.size - pos):  # n * (
        rotate(queue)  # 27
    # ) = 27n

    return el


def push_by_pos(queue: Queue, el: Real, pos: int) -> None:  # $CX_DEF: 54*n + 18$
    assert pos <= queue.size and pos >= 0, "Invalid position!"  # 5

    for _ in range(pos):  # n * (
        rotate(queue)  # 27
    # ) = 27n

    queue.push(el)  # 13

    for _ in range(queue.size - pos - 1):  # n * (
        rotate(queue)  # 27
    # ) = 27n


def push_back(queue: Queue, el: Real) -> None:  # $CX_DEF: 13$
    queue.push(el)  # 13


def push_front(queue: Queue, el: Real) -> None:  # $CX_DEF: 27*n + 13$
    queue.push(el)  # 13
    for _ in range(queue.size - 1):  # n * (
        rotate(queue)  # 27
    # ) = 27n


def pop_back(queue: Queue) -> Real:  # $CX_DEF: 27*n + 14$
    for _ in range(queue.size - 1):  # n * (
        rotate(queue)  # 27
    # ) = 27n
    return queue.pop()  # 14


def pop_front(queue: Queue) -> Real:  # $CX_DEF: 14$
    return queue.pop()  # 14


def swap(queue: Queue, pos1: int, pos2: int) -> None:  #  $CX_DEF: 216*n + 74$
    temp = pop_by_pos(queue, pos1)  # 54n + 19
    push_by_pos(queue, pop_by_pos(queue, pos2 - 1), pos1)  # 108n + 37
    push_by_pos(queue, temp, pos2)  # 54n + 18


def partition(queue: Queue, l: int = 0, r: int = -1) -> Queue:  # $CX_DEF: 99*n + 6$
    buff = Queue()  # 2

    if r == -1:  # 1
        r = queue.size - 1  # 3

    for _ in range(l):  # n * (
        rotate(queue)  # 27
    # ) = 27n

    for _ in range(r - l + 1):  # n * (
        buff.push(queue.head)  # 18
        rotate(queue)  # 27
    # ) = 45n

    for _ in range(queue.size - r - 1):  # n * (
        rotate(queue)  # 27
    # ) = 27n

    return buff


# $ENDEF
from random import randint  # ignore: E402

import pytest  # ignore: E402

Collection = Queue


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
