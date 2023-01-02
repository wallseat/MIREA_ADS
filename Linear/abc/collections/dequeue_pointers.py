# $Collection: Dequeue$
# $DEF
from typing import Generic, List, Optional, TypeVar

VT = TypeVar("VT")


class Node(Generic[VT]):
    value: VT
    next: Optional["Node"] = None
    prev: Optional["Node"] = None

    def __init__(self, value: VT):
        self.value = value

    def __repr__(self) -> str:
        return str(self.value)


class Dequeue(Generic[VT]):
    _head: Optional[Node[VT]]
    _tail: Optional[Node[VT]]
    _size: int
    _n_op: int

    def __init__(self) -> None:
        self._head = None
        self._tail = None
        self._size = 0
        self._n_op = 0

    def push_back(self, value: VT) -> None:  # 11
        node = Node[VT](value)  # 2

        if self.empty:  # 2
            self._head = node  # 2
            self._tail = node  # 2

            self._n_op += 6

        else:
            self._tail.next = node  # 3
            node.prev = self._tail  # 3
            self._tail = node  # 2

            self._n_op += 10

        self._size += 1  # 1

        self._n_op += 1

    def push_front(self, value: VT) -> None:  # 11
        node = Node[VT](value)

        if self.empty:  # 2
            self._head = node  # 2
            self._tail = node  # 2

            self._n_op += 6

        else:
            self._head.prev = node  # 3
            node.next = self._head  # 3
            self._head = node  # 2

            self._n_op += 10

        self._size += 1  # 1

        self._n_op += 1

    def pop_back(self) -> VT:  # 14
        assert not self.empty, "Can't pop from empty dequeue!"  # 2

        node = self._tail  # 2
        if self.size == 1:
            self._head = None
            self._tail = None

        else:
            self._tail = node.prev  # 3
            self._tail.next = None  # 3
            node.prev = None  # 2

        self._size -= 1  # 2

        self._n_op += 11

        return node.value

    def pop_front(self) -> VT:  # 14
        assert not self.empty, "Can't pop from empty dequeue!"  # 2

        node = self._head  # 2

        if self.size == 1:
            self._head = None
            self._tail = None

        else:
            self._head = node.next  # 3
            self._head.prev = None  # 3
            node.next = None  # 2

        self._size -= 1  # 2

        self._n_op += 12

        return node.value

    def push(self, value: VT) -> None:  # $CX_DEF: 11$
        self.push_back(value)

    def pop(self) -> VT:  # $CX_DEF: 14$
        return self.pop_front()

    @property
    def size(self) -> int:  # 1
        return self._size

    @property
    def head(self) -> VT:  # 4
        assert not self.empty, "Can't get head from empty dequeue!"  # 2

        return self._head.value

    @property
    def tail(self) -> VT:  # 4
        assert not self.empty, "Can't get tail from empty dequeue!"  # 2

        return self._tail.value

    @property
    def n_op(self) -> int:
        return self._n_op

    @property
    def empty(self) -> bool:  # $CX_DEF: 2$
        return self._size == 0


def print_dequeue(dequeue: Dequeue[VT]) -> None:
    elements = []
    for _ in range(dequeue.size):
        elements.append(dequeue.head)
        rotate_left(dequeue)

    print("Dequeue[" + ", ".join(map(str, elements)) + "]")


def rotate_left(dequeue: Dequeue[VT]) -> None:  # 25
    dequeue.push_back(dequeue.pop_front())


def rotate_right(dequeue: Dequeue[VT]) -> None:  # 25
    dequeue.push_front(dequeue.pop_back())


def seek(dequeue: Dequeue[VT], pos: int) -> VT:  # $CX_DEF: 26*n + 12$
    assert pos <= dequeue.size and pos >= 0, "Invalid position!"  # 5

    if pos >= dequeue.size // 2:  # 3
        for _ in range(dequeue.size - pos - 1):  # (n / 2) * (
            rotate_right(dequeue)  # 25
        # ) = 13n

        node = dequeue.tail  # 4

        for _ in range(dequeue.size - pos - 1):  # (n / 2) * (
            rotate_left(dequeue)  # 25
        # ) = 13n

        return node

    else:
        for _ in range(pos):  # (n / 2) * (
            rotate_left(dequeue)  # 25
        # ) = 13n

        node = dequeue.head  # 4

        for _ in range(pos):  # (n / 2) * (
            rotate_right(dequeue)  # 25
        # ) = 13n

        return node


def push_by_pos(dequeue: Dequeue[VT], el: VT, pos: int) -> None:  # $CX_DEF: 26*n + 19$
    assert pos <= dequeue.size and pos >= 0, "Invalid position!"  # 5

    if pos == dequeue.size:  # 2
        dequeue.push_back(el)

    elif pos == 0:  # 1
        dequeue.push_front(el)

    else:
        if pos < dequeue.size // 2:  # 3
            for _ in range(pos):  # (n // 2) * (
                rotate_left(dequeue)  # 25
            # ) = 13n

            dequeue.push_front(el)  # 11

            for _ in range(pos):  # (n // 2) * (
                rotate_right(dequeue)  # 25
            # ) = 13n

        else:
            for _ in range(dequeue.size - pos):
                rotate_right(dequeue)

            dequeue.push_back(el)

            for _ in range(dequeue.size - pos - 1):
                rotate_left(dequeue)


def pop_by_pos(dequeue: Dequeue[VT], pos: int) -> VT:  # $CX_DEF: 26*n + 23$
    assert pos <= dequeue.size and pos >= 0, "Invalid position!"  # 5

    if pos == dequeue.size - 1:  # 3
        return dequeue.pop_back()  # 14

    elif pos == 0:  # 1
        return dequeue.pop_front()  # 14

    else:
        if pos < dequeue.size // 2:  # 3
            for _ in range(pos):  # n // 2 * (
                rotate_left(dequeue)  # 25
            # ) = 13n

            v = dequeue.pop_front()  # 14

            for _ in range(pos):  # n // 2 * (
                rotate_right(dequeue)  # 25
            # ) = 13n

        else:
            for _ in range(dequeue.size - pos - 1):
                rotate_right(dequeue)

            v = dequeue.pop_back()

            for _ in range(dequeue.size - pos):
                rotate_left(dequeue)

        return v


def push_front(dequeue: Dequeue[VT], el: VT) -> None:  # $CX_DEF: 11$
    dequeue.push_front(el)


def push_back(dequeue: Dequeue[VT], el: VT) -> None:  # $CX_DEF: 11$
    dequeue.push_back(el)


def pop_front(dequeue: Dequeue[VT]) -> VT:  # $CX_DEF: 12$
    return dequeue.pop_front()


def pop_back(dequeue: Dequeue[VT]) -> VT:  # $CX_DEF: 12$
    return dequeue.pop_back()


def swap(dequeue: Dequeue, pos1: int, pos2: int) -> None:  # $CX_DEF: 52*n + 62$
    left_el_pos, right_el_pos = min(pos1, pos2), max(pos1, pos2)  # 4

    assert left_el_pos >= 0 and right_el_pos <= dequeue.size, "Invalid position argument!"  # 5

    if left_el_pos < dequeue.size // 2:  # 3
        for _ in range(left_el_pos):  #  (n // 2) * (
            rotate_left(dequeue)  # 25
        # ) = 13n

        left_el = dequeue.pop_front()  # 14

        for _ in range(right_el_pos - left_el_pos - 1):  # (n // 2) * (
            rotate_left(dequeue)  # 25
        # ) = 13n

        right_el = dequeue.pop_front()  # 14

        dequeue.push_front(left_el)  # 11

        for _ in range(right_el_pos - left_el_pos - 1):  # (n // 2) * (
            rotate_right(dequeue)  # 25
        # ) = 13n

        dequeue.push_front(right_el)  # 11

        for _ in range(left_el_pos):  # (n // 2) * (
            rotate_right(dequeue)  # 25
        # ) = 13n

    else:
        for _ in range(dequeue.size - right_el_pos - 1):
            rotate_right(dequeue)

        left_el = dequeue.pop_back()

        for _ in range(right_el_pos - left_el_pos - 1):
            rotate_right(dequeue)

        right_el = dequeue.pop_back()

        dequeue.push_back(left_el)

        for _ in range(right_el_pos - left_el_pos - 1):
            rotate_left(dequeue)

        dequeue.push_back(right_el)

        for _ in range(dequeue.size - right_el_pos - 1):
            rotate_left(dequeue)


def partition(dequeue: Dequeue[VT], l: int = 0, r: int = -1) -> Dequeue[VT]:  # $CX_DEF: 88*n + 6$
    buffer = Dequeue[VT]()  # 2

    if r == -1:  # 1
        r = dequeue.size - 1  # 3

    for _ in range(l):  # n * (
        rotate_left(dequeue)  # 25
    # ) = 25n

    for _ in range(r - l + 1):  # n * (
        buffer.push_back(dequeue.head)  # 13
        rotate_left(dequeue)  # 25
    # ) = 38n

    for _ in range(dequeue.size - r - 1):  # n * (
        rotate_left(dequeue)  # 25
    # ) = 25n

    return buffer


# $ENDEF

from random import randint  # ignore: E402

import pytest  # ignore: E402

Collection = Dequeue[int]


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

    data.insert(17, 20)
    push_by_pos(collection, 20, 17)

    for i, el in enumerate(data):
        assert seek(collection, i) == el


def test_pop_by_pos(data: List, collection: Collection):
    data.pop(2)
    pop_by_pos(collection, 2)

    data.pop(16)
    pop_by_pos(collection, 16)

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
