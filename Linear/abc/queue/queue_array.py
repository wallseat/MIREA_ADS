from typing import Generic, List, TypeVar

VT = TypeVar("VT")


class Queue(Generic[VT]):
    _queue: List[VT]
    _bias: int
    _size: int
    _max_size: int
    _n_op: int

    def __init__(self, max_size: int = 10000) -> None:
        self._queue = [None for _ in range(max_size)]
        self._max_size = max_size
        self._size = 0
        self._n_op = 0
        self._bias = 0

    def push(self, value: VT) -> None:  # 8
        if self._size == self._max_size:  # 3
            raise RuntimeError("Queue overflow")

        self._queue[(self._size + self._bias) % self._max_size] = value  # 3
        self._size += 1  # 2

        self._n_op += 8

    def pop(self) -> VT:  # 12

        if self.is_empty():
            raise Exception("Can't pop from empty queue!")

        el = self._queue[self._bias]  # 4
        self._size -= 1  # 2
        self._bias = (self._bias + 1) % self._max_size  # 6

        self._n_op += 12

        return el

    def is_empty(self) -> bool:  # 2
        return self._size == 0

    @property
    def size(self) -> int:  # 1
        return self._size

    @property
    def tail(self) -> VT:  # 8
        return self._queue[(self._size - 1 + self._bias) % self._max_size]

    @property
    def head(self) -> VT:  # 3
        return self._queue[self._bias]

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


def rotate(queue: Queue[VT]) -> None:  # 20
    queue.push(queue.pop())  # 20


def seek(queue: Queue[VT], pos: int) -> VT:  # 40n + 20
    for _ in range(pos):  # n * (
        rotate(queue)  # 20
    # ) = 20n

    el = queue.pop()  # 12
    queue.push(el)  # 8

    for _ in range(queue.size - pos - 1):  # n * (
        rotate(queue)  # 20
    # ) = 20n

    return el


def pop_by_pos(queue: Queue[VT], pos: int) -> VT:  # 40n + 12
    for _ in range(pos):  # n * (
        rotate(queue)  # 20
    # ) = 20n

    el = queue.pop()  # 12

    for _ in range(queue.size - pos):  # n * (
        rotate(queue)  # 20
    # ) = 20n

    return el


def push_by_pos(queue: Queue[VT], el: VT, pos: int) -> None:  # 40n + 10
    if pos >= queue.size:  # 2
        queue.push(el)  # 8
        return

    for _ in range(pos):  # n * (
        rotate(queue)  # 20
    # ) = 20n

    queue.push(el)  # 8

    for _ in range(queue.size - pos - 1):  # n * (
        rotate(queue)  # 20
    # ) = 20n


def swap(queue: Queue[VT], pos1: int, pos2: int) -> None:  #  160n + 46
    temp = pop_by_pos(queue, pos1)  # 40n + 13
    push_by_pos(queue, pop_by_pos(queue, pos2 - 1), pos1)  # 80 + 23
    push_by_pos(queue, temp, pos2)  # 40n + 10


def slice_(queue: Queue[VT], l: int = 0, r: int = -1) -> Queue[VT]:  # 68n + 6
    buff = Queue[VT](max_size=queue.size)  # 2

    if r == -1:  # 1
        r = queue.size - 1  # 3

    for _ in range(l):  # n * (
        rotate(queue)  # 20
    # ) = 20n

    for _ in range(r - l + 1):  # n * (
        buff.push(queue.head)  # 8
        rotate(queue)  # 20
    # ) = 28n

    for _ in range(queue.size - r - 1):  # n * (
        rotate(queue)  # 20
    # ) = 20n

    return buff


if __name__ == "__main__":
    from random import randint

    queue = Queue[int]()
    test_data = [randint(-100, 100) for _ in range(20)]

    for el in test_data:
        queue.push(el)

    print_queue(queue)

    # 1
    for i, el in enumerate(test_data):
        assert seek(queue, i) == el

    # 2
    test_data.insert(2, 20)
    push_by_pos(queue, 20, 2)

    for i, el in enumerate(test_data):
        assert seek(queue, i) == el

    # 3
    test_data.pop(2)
    pop_by_pos(queue, 2)
    for i, el in enumerate(test_data):
        assert seek(queue, i) == el

    # 4
    tmp = test_data[2]
    test_data[2] = test_data[5]
    test_data[5] = tmp

    swap(queue, 2, 5)
    for i, el in enumerate(test_data):
        assert seek(queue, i) == el

    # 5
    slice = slice_(queue, 5, 15)
    for i, el in enumerate(test_data[5:16]):
        assert seek(queue, i + 5) == el

    # 6
    for _ in test_data:
        queue.pop()

    assert queue.size == 0
    assert queue.is_empty() == True

    print("All tests passed")
