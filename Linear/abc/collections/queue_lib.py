# $Collection: Queue$
# $DEF
from queue import SimpleQueue
from typing import List, TypeVar

VT = TypeVar("VT")


class Queue(SimpleQueue):
    _n_op: int

    def __init__(self) -> None:
        super(SimpleQueue, self).__init__()

        self._n_op = 0

    def push(self, el: VT) -> None:  # $CX_DEF: 1$
        self.put(el)  # 1
        self._n_op += 1

    def pop(self) -> VT:  # $CX_DEF: 3$
        assert not self.empty, "Can't pop from empty queue!"  # 2

        v = self.get()  # 1
        self._n_op += 3

        return v

    @property
    def empty(self) -> bool:  # $CX_DEF: 1$
        return super().empty()

    @property
    def n_op(self) -> int:
        return self._n_op

    @property
    def size(self) -> int:  # 1
        return self.qsize()


def print_queue(queue: Queue[VT]) -> None:
    elements = []
    for _ in range(queue.size):
        el = queue.pop()
        elements.append(el)
        queue.push(el)

    print("Queue[" + ", ".join(map(str, elements)) + "]")


def rotate(queue: Queue[VT]) -> None:  # 4
    queue.push(queue.pop())  # 4


def seek(queue: Queue[VT], pos: int) -> VT:  # $CX_DEF: 8*n + 5$
    assert pos <= queue.size and pos >= 0, "Invalid position!"  # 5

    for _ in range(pos):  # n * (
        rotate(queue)  # 4
    # ) = 4n

    el = queue.pop()  # 3
    queue.push(el)  # 1

    for _ in range(queue.size - pos - 1):  # (n - 1) * (
        rotate(queue)  # 4
    # ) = 4n - 4

    return el


def pop_by_pos(queue: Queue[VT], pos: int) -> VT:  # $CX_DEF: 8*n + 8$
    assert pos <= queue.size and pos >= 0, "Invalid position!"  # 5

    for _ in range(pos):  # n * (
        rotate(queue)  # 4
    # ) = 4n

    el = queue.pop()  # 3

    for _ in range(queue.size - pos):  # n * (
        rotate(queue)  # 4
    # ) = 4n

    return el


def push_by_pos(queue: Queue[VT], el: VT, pos: int) -> None:  # CX_DEF: 8*n + 2$
    assert pos <= queue.size and pos >= 0, "Invalid position!"  # 5

    for _ in range(pos):  # n * (
        rotate(queue)  # 4
    # ) = 4n

    queue.push(el)  # 1

    for _ in range(queue.size - pos - 1):  # (n - 1) * (
        rotate(queue)  # 4
    # ) = 4n - 4


def push_back(queue: Queue[VT], el: VT) -> None:  # $CX_DEF: 1$
    queue.push(el)  # 1


def push_front(queue: Queue[VT], el: VT) -> None:  # $CX_DEF: 4*n + 1$
    queue.push(el)  # 1
    for _ in range(queue.size - 1):  # n * (
        rotate(queue)  # 4
    # ) = 4n


def pop_back(queue: Queue[VT]) -> VT:  # $CX_DEF: 4*n + 3$
    for _ in range(queue.size - 1):  # n * (
        rotate(queue)  # 4
    # ) = 4n
    return queue.pop()  # 3


def pop_front(queue: Queue[VT]) -> VT:  # $CX_DEF: 1$
    return queue.pop()  # 1


def swap(queue: SimpleQueue, pos1: int, pos2: int):  # $CX_DEF: 32*n + 20$
    temp = pop_by_pos(queue, pos1)  # 8n + 8
    push_by_pos(queue, pop_by_pos(queue, pos2 - 1), pos1)  # 16n + 10
    push_by_pos(queue, temp, pos2)  # 8n + 2


def slice_(queue: Queue[VT], l: int = 0, r: int = -1) -> Queue[VT]:  # $CX_DEF: 13*n + 2$
    buffer = Queue[VT]()  # 2

    if r == -1:  # 1
        r = queue.size - 1  # 3

    for _ in range(l):  # n * (
        rotate(queue)  # 4
    # ) = 4n

    for _ in range(r - l + 1):  # n * (
        el = queue.pop()  # 3

        buffer.push(el)  # 1

        queue.push(el)  # 1
    # ) = 5n

    for _ in range(queue.size - r - 1):  # (n - 1) * (
        rotate(queue)  # 4
    # ) = 4n - 4

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
