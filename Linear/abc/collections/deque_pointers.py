from typing import Generic, Optional, TypeVar, List

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

    def pop_back(self) -> VT:  # 12
        if self.empty:
            raise Exception("Can't pop from empty dequeue!")

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

    def pop_front(self) -> VT:  # 12
        if self.empty:
            raise Exception("Can't pop from empty dequeue!")

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

    @property
    def size(self) -> int:  # 1
        return self._size

    @property
    def head(self) -> VT:  # 2
        return self._head.value

    @property
    def tail(self) -> VT:  # 2
        return self._tail.value

    @property
    def n_op(self) -> int:
        return self._n_op
    
    @property
    def empty(self) -> bool:  # 2
        return self._size == 0


def print_dequeue(dequeue: Dequeue[VT]) -> None:
    elements = []
    for _ in range(dequeue.size):
        elements.append(dequeue.head)
        rotate_left(dequeue)

    print("Dequeue[" + ", ".join(map(str, elements)) + "]")


def rotate_left(dequeue: Dequeue[VT]) -> None:  # 23
    dequeue.push_back(dequeue.pop_front())


def rotate_right(dequeue: Dequeue[VT]) -> None:  # 23
    dequeue.push_front(dequeue.pop_back())


def seek(dequeue: Dequeue[VT], index: int) -> VT:  # 48n + 12
    if dequeue.empty:  # 2
        raise Exception("Can't seek empty dequeue!")

    if index >= dequeue.size:  # 3
        raise Exception("Index out of range!")

    if index >= dequeue.size // 2:  # 3
        for _ in range(dequeue.size - index - 1):  # (n / 2) * (
            rotate_right(dequeue)  # 23
        # ) = 12n

        node = dequeue.tail  # 2

        for _ in range(dequeue.size - index - 1):  # (n / 2) * (
            rotate_left(dequeue)  # 23
        # ) = 12n

        return node

    else:
        for _ in range(index):  # (n / 2) * (
            rotate_left(dequeue)  # 23
        # ) = 12n

        node = dequeue.head  # 2

        for _ in range(index):  # (n / 2) * (
            rotate_right(dequeue)  # 23
        # ) = 12n

        return node


def push_by_pos(dequeue: Dequeue[VT], el: VT, pos: int) -> None:  # 24n + 17
    if pos < 0 or pos > dequeue.size:  # 4
        raise Exception("Invalid position argument!")

    if pos == dequeue.size:  # 2
        dequeue.push_back(el)

    elif pos == 0:  # 1
        dequeue.push_front(el)

    else:
        if pos < dequeue.size // 2:  # 3
            for _ in range(pos):  # (n // 2) * (
                rotate_left(dequeue)  # 23
            # ) = 12n

            dequeue.push_front(el)  # 11

            for _ in range(pos):  # (n // 2) * (
                rotate_right(dequeue)  # 23
            # ) = 12n

        else:
            for _ in range(dequeue.size - pos):
                rotate_right(dequeue)

            dequeue.push_back(el)

            for _ in range(dequeue.size - pos):
                rotate_left(dequeue)


def pop_by_pos(dequeue: Dequeue[VT], i: int) -> VT:  # 24n + 17
    if i < 0 or i >= dequeue.size:
        raise Exception("Invalid position argument!")

    if i == dequeue.size - 1:
        return dequeue.pop_back()

    elif i == 0:
        return dequeue.pop_front()

    else:
        if i < dequeue.size // 2:
            for _ in range(i):
                rotate_left(dequeue)

            v = dequeue.pop_front()

            for _ in range(i):
                rotate_right(dequeue)

        else:
            for _ in range(dequeue.size - i - 1):
                rotate_right(dequeue)

            v = dequeue.pop_back()

            for _ in range(dequeue.size - i - 1):
                rotate_left(dequeue)

        return v

def push_front(dequeue: Dequeue[VT], el: VT) -> None:  # 11
    dequeue.push_front(el)

def push_back(dequeue: Dequeue[VT], el: VT) -> None:  # 11
    dequeue.push_back(el)
    
def pop_front(dequeue: Dequeue[VT]) -> VT:  # 12
    return dequeue.pop_front()

def pop_back(dequeue: Dequeue[VT]) -> VT:  # 12
    return dequeue.pop_back()

def swap(dequeue: Dequeue, pos1: int, pos2: int) -> None:  # 92n + 10
    left_el_pos, right_el_pos = min(pos1, pos2), max(pos1, pos2)  # 4

    if left_el_pos < 0 or right_el_pos >= dequeue.size:  # 3
        raise Exception("Invalid position argument!")

    if left_el_pos < dequeue.size // 2:  # 3
        for _ in range(left_el_pos):  #  n * (
            rotate_left(dequeue)  # 23
        # ) = 23n

        left_el = dequeue.pop_front()  # 12

        for _ in range(right_el_pos - left_el_pos - 1):  # n * (
            rotate_left(dequeue)  # 23
        # ) = 23n

        right_el = dequeue.pop_front()  # 12

        dequeue.push_front(left_el)  # 11

        for _ in range(right_el_pos - left_el_pos - 1):  # n * (
            rotate_right(dequeue)  # 23
        # ) = 23n

        dequeue.push_front(right_el)  # 11

        for _ in range(left_el_pos):  # n * (
            rotate_right(dequeue)  # 23
        # ) = 23n

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


def slice_(dequeue: Dequeue[VT], l: int = 0, r: int = -1) -> Dequeue[VT]:  # 82n + 6
    buffer = Dequeue[VT]()  # 2

    if r == -1:  # 1
        r = dequeue.size - 1  # 3

    for _ in range(l):  # n * (
        rotate_left(dequeue)  # 23
    # ) = 23n

    for _ in range(r - l + 1):  # n * (
        buffer.push_back(dequeue.head)  # 13
        rotate_left(dequeue)  # 23
    # ) = 36n

    for _ in range(dequeue.size - r - 1):  # n * (
        rotate_left(dequeue)  # 23
    # ) = 23n

    return buffer


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