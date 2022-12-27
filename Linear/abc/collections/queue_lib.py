from queue import SimpleQueue
from typing import TypeVar

VT = TypeVar("VT")


class Queue(SimpleQueue):
    _n_op: int

    def __init__(self) -> None:
        super(SimpleQueue, self).__init__()

        self._n_op = 0

    def push(self, el: VT) -> None:  # 1
        self.put(el)  # 1
        self._n_op += 1

    def pop(self) -> VT:  # 1
        v = self.get()  # 1
        self._n_op += 1

        return v

    def is_empty(self) -> bool:
        return self.empty()

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


def rotate(queue: Queue[VT]) -> None:  # 2
    queue.push(queue.pop())  # 2


def seek(queue: Queue[VT], pos: int) -> VT:  # 4n + 1
    for _ in range(pos):  # n * (
        rotate(queue)  # 2
    # ) = 2n

    el = queue.pop()  # 2
    queue.push(el)  # 1

    for _ in range(queue.size - pos - 1):  # (n - 1) * (
        rotate(queue)  # 2
    # ) = 2n - 2

    return el


def pop_by_pos(queue: Queue[VT], pos: int) -> VT:  # 4n + 2
    for _ in range(pos):  # n * (
        rotate(queue)  # 2
    # ) = 2n

    el = queue.pop()  # 2

    for _ in range(queue.size - pos):  # n * (
        rotate(queue)  # 2
    # ) = 2n

    return el


def push_by_pos(queue: Queue[VT], el: VT, pos: int) -> None:  # 4n - 1
    if pos >= queue.size:  # 2
        queue.push(el)  # 1

        return

    for _ in range(pos):  # n * (
        rotate(queue)  # 2
    # ) = 2n

    queue.push(el)  # 1

    for _ in range(queue.size - pos - 1):  # (n - 1) * (
        rotate(queue)  # 2
    # ) = 2n - 2


def swap(queue: SimpleQueue, pos1: int, pos2: int):  # 16n + 2
    temp = pop_by_pos(queue, pos1)  # 4n + 2
    push_by_pos(queue, pop_by_pos(queue, pos2 - 1), pos1)  # 8n + 1
    push_by_pos(queue, temp, pos2)  # 4n - 1


def slice_(queue: Queue[VT], l: int = 0, r: int = -1) -> Queue[VT]:  # 7n + 4
    buffer = Queue[VT]()  # 2

    if r == -1:  # 1
        r = queue.size - 1  # 3

    for _ in range(l):  # n * (
        rotate(queue)  # 2
    # ) = 2n

    for _ in range(r - l + 1):  # n * (
        el = queue.pop()  # 1

        buffer.push(el)  # 1

        queue.push(el)  # 1
    # ) = 3n

    for _ in range(queue.size - r - 1):  # (n - 1) * (
        rotate(queue)  # 2
    # ) = 2n - 2

    return buffer


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
