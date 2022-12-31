from typing import Generic, List, TypeVar

VT = TypeVar("VT")


class Queue(Generic[VT]):
    _queue: List[VT]
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

    def push(self, value: VT) -> None:  # 13
        if self._size == self._array_size:  # 3
            self._queue += [0] * self._array_size  # 3
            self._array_size *= 2  # 2

        self._queue[(self._size + self._bias) % self._array_size] = value  # 3
        self._size += 1  # 2

        self._n_op += 13

    def pop(self) -> VT:  # 14
        assert not self.empty, "Can't pop from empty queue!"  # 2

        el = self._queue[self._bias]  # 4
        self._size -= 1  # 2
        self._bias = (self._bias + 1) % self._array_size  # 6

        self._n_op += 14

        return el

    @property
    def empty(self) -> bool:  # 2
        return self._size == 0

    @property
    def size(self) -> int:  # 1
        return self._size

    @property
    def tail(self) -> VT:  # 10
        assert not self.empty, "Can't get head from empty dequeue!"  # 2

        self._n_op += 10

        return self._queue[(self._size - 1 + self._bias) % self._max_size]

    @property
    def head(self) -> VT:  # 5
        assert not self.empty, "Can't get tail from empty dequeue!"  # 2

        self._n_op += 5

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


def rotate(queue: Queue[VT]) -> None:  # 27
    queue.push(queue.pop())  # 27


def seek(queue: Queue[VT], pos: int) -> VT:  # 54*n + 32
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


def pop_by_pos(queue: Queue[VT], pos: int) -> VT:  # 54*n + 19
    assert pos <= queue.size and pos >= 0, "Invalid position!"  # 5

    for _ in range(pos):  # n * (
        rotate(queue)  # 27
    # ) = 27n

    el = queue.pop()  # 14

    for _ in range(queue.size - pos):  # n * (
        rotate(queue)  # 27
    # ) = 27n

    return el


def push_by_pos(queue: Queue[VT], el: VT, pos: int) -> None:  # 54*n + 18
    assert pos <= queue.size and pos >= 0, "Invalid position!"  # 5

    for _ in range(pos):  # n * (
        rotate(queue)  # 27
    # ) = 27n

    queue.push(el)  # 13

    for _ in range(queue.size - pos - 1):  # n * (
        rotate(queue)  # 27
    # ) = 27n


def push_back(queue: Queue[VT], el: VT) -> None:  # 13
    queue.push(el)  # 13


def push_front(queue: Queue[VT], el: VT) -> None:  # 27*n + 13
    queue.push(el)  # 13
    for _ in range(queue.size - 1):  # n * (
        rotate(queue)  # 27
    # ) = 27n


def pop_back(queue: Queue[VT]) -> VT:  # 27*n + 14
    for _ in range(queue.size - 1):  # n * (
        rotate(queue)  # 27
    # ) = 27n
    return queue.pop()  # 14


def pop_front(queue: Queue[VT]) -> VT:  # 14
    return queue.pop()  # 14


def swap(queue: Queue[VT], pos1: int, pos2: int) -> None:  #  216*n + 74
    temp = pop_by_pos(queue, pos1)  # 54n + 19
    push_by_pos(queue, pop_by_pos(queue, pos2 - 1), pos1)  # 108n + 37
    push_by_pos(queue, temp, pos2)  # 54n + 18


def slice_(queue: Queue[VT], l: int = 0, r: int = -1) -> Queue[VT]:  # 99*n + 6
    buff = Queue[VT]()  # 2

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


def selection_sort(queue: Queue[VT]) -> Queue[VT]:  # 54*n**3 + 306*n**2 + 108*n
    for start_pos in range(queue.size):  # n * (
        min_el_pos = start_pos  # 1
        min_el = seek(queue, min_el_pos)  # 54*n + 33

        for check_el_pos in range(start_pos + 1, queue.size):  # n * (
            check_el = seek(queue, check_el_pos)  # 54*n + 33
            if check_el < min_el:  # 1
                min_el = check_el  # 1
                min_el_pos = check_el_pos  # 1
        # ) = 54*n**2 + 36*n

        if min_el_pos != start_pos:  # 1
            swap(queue, start_pos, min_el_pos)  # 216*n + 74
    # ) = 54*n**3 + 306*n**2 + 108*n


if __name__ == "__main__":
    from random import randint

    data = [randint(-99, 99) for _ in range(100)]
    queue = Queue[int]()
    for el in data:
        queue.push(el)
    data.sort()
    selection_sort(queue)
    for i, el in enumerate(data):
        assert el == seek(queue, i), f"index: {i}, expected {el}, got {seek(queue, i)}"
