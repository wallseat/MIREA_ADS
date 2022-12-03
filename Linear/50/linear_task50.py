from typing import Generic, TypeVar, Optional

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

    def push(self, value: VT):  # 5
        node = Node(value)

        if self.is_empty():  # 1
            self._head = node  # 1
            self._tail = node  # 1
        else:
            self._tail.next = node  # 2
            self._tail = node  # 1

        self._size += 1  # 1
        self._n_op += 4

    def pop(self) -> VT:  # 6
        if self.is_empty():  # 1
            raise Exception("Can't pop from empty queue!")

        node = self._head  # 1
        self._head = node.next  # 2

        if self._head is None:  # 1
            self._tail = None  # 1

        self._size -= 1  # 1
        self._n_op += 6

        return node.value

    def is_empty(self) -> bool:  # 1
        return self._size == 0

    @property
    def head(self) -> VT:  # 1
        return self._head.value

    @property
    def tail(self) -> VT:  # 1
        return self._tail.value

    @property
    def size(self) -> int:  # 1
        return self._size

    @property
    def n_op(self) -> int:  # 1
        return self._n_op


def print_queue(queue: Queue):
    elems = []
    for _ in range(queue.size):
        elems.append(queue.head)
        rotate(queue)

    print("Queue[" + ", ".join(map(str, elems)) + "]")


def rotate(queue: Queue):  # 11
    queue.push(queue.pop())


def seek(queue: Queue[VT], pos: int) -> VT:  # 11n + 2
    for _ in range(pos):  # 11pos
        rotate(queue)

    el = queue.head  # 2

    for _ in range(queue.size - pos):  # 11n - 11pos
        rotate(queue)

    return el


def pop_by_pos(queue: Queue[VT], pos: int) -> VT:  # 11n + 6
    for _ in range(pos):  # 11pos
        rotate(queue)

    el = queue.pop()  # 6

    for _ in range(queue.size - pos):  # 11n - 11pos
        rotate(queue)

    return el


def push_by_pos(queue: Queue[VT], el: VT, pos: int):  # 11n - 3
    if pos >= queue.size:  # 2
        queue.push(el)  # 5
        return

    for _ in range(pos):  # 11pos
        rotate(queue)

    queue.push(el)  # 6

    for _ in range(queue.size - pos - 1):  # 11n - 11pos - 11
        rotate(queue)


def swap(queue: Queue, pos1: int, pos2: int):  # 44n + 6
    temp = pop_by_pos(queue, pos1)  # 11n + 6
    push_by_pos(queue, pop_by_pos(queue, pos2 - 1), pos1)  # 22n + 3
    push_by_pos(queue, temp, pos2)  # 11n - 3


def heapify(
    queue: Queue, n: int, i: int
):  # (7 + 22n + 8 + 22n + 8 + 1 + 44n + 6) * log(n) = 88n * log(n) + 30log(n)
    largest = i  # 1
    l = 2 * i + 1  # 3
    r = 2 * i + 2  # 3

    if l < n and seek(queue, i) < seek(
        queue, l
    ):  # 1 + 1 + 11n + 2 + 1 + 11n + 2 = 22n + 7
        largest = l  # 1

    if r < n and seek(queue, largest) < seek(
        queue, r
    ):  # 1 + 1 + 11n + 2 + 1 + 11n + 2 = 22n + 7
        largest = r  # 1

    if largest != i:  # 1
        swap(queue, i, largest)  # 44n + 6
        heapify(queue, n, largest)  # ~log(n)


def heap_sort(queue: Queue):
    # 1 + 44n^2 * log(n) + 15n * log(n) + 44n^2 + 6n + 88n^2 * log(n) + 30n * log(n) =
    # = 132n^2 * log(n) + 45n * log(n) + 21n + 1
    n = queue.size  # 1

    for i in range(
        n // 2 - 1, -1, -1
    ):  # (n / 2) * (88n * log(n) + 30log(n)) = 44n^2 * log(n) + 15n * log(n)
        heapify(queue, n, i)

    for i in range(n - 1, 0, -1):  # n * (
        swap(queue, 0, i)  # 44n + 6
        heapify(queue, i, 0)  # 88n * log(n) + 30log(n)
    # ) = 44n^2 + 6n + 88n^2 * log(n) + 30n * log(n)


if __name__ == "__main__":
    import time
    from random import randint

    tests = 10
    step = 100

    for test_num in range(1, tests + 1):
        N_OP = 0
        queue = Queue[int]()
        for _ in range(test_num * step):
            queue.push(randint(-10000, 10000))

        start_time = time.time()
        heap_sort(queue)
        total_time = time.time() - start_time

        print(f"Test: {test_num}")
        print(f"Elems count: {test_num * step}")
        print(f"Total time: {total_time}")
        print(f"N_OP: {queue.n_op}")
        print("-------------")
