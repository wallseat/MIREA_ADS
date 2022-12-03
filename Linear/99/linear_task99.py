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
    _size: int
    _n_op: int

    def __init__(self):
        self._head = None
        self._size = 0
        self._n_op = 0

    def push(self, value: VT):  # 2n + 6
        node = Node(value)

        if self.is_empty():  # 1
            self._head = node  # 1
        else:
            tail = self._head  # 2
            while tail.next:  # 2n
                tail = tail.next
            tail.next = node  # 2

        self._size += 1  # 1
        self._n_op += (self._size - 1) * 2 + 6

    def pop(self) -> VT:  # 4
        if self.is_empty():  # 1
            raise Exception("Can't pop from empty queue!")

        node = self._head  # 1
        self._head = node.next  # 2

        self._size -= 1  # 1
        self._n_op += 4

        return node.value

    def is_empty(self) -> bool:
        return self._size == 0

    @property
    def head(self) -> VT:
        return self._head.value

    @property
    def size(self) -> int:
        return self._size

    @property
    def n_op(self) -> int:
        return self._n_op


def print_queue(queue: Queue):
    elems = []
    for _ in range(queue.size):
        el = queue.pop()
        elems.append(el)
        queue.push(el)

    print("Queue[" + ", ".join(map(str, elems)) + "]")


def print_queue(queue: Queue):
    elems = []
    for _ in range(queue.size):
        elems.append(queue.head)
        rotate(queue)

    print("Queue[" + ", ".join(map(str, elems)) + "]")


def rotate(queue: Queue):  # 2n + 10
    queue.push(queue.pop())


def seek(queue: Queue[VT], pos: int) -> VT:  # 2n^2 + 10n + 2
    for _ in range(pos):  # (2n + 10)pos = 2n * pos + 10pos
        rotate(queue)

    el = queue.head  # 2

    for _ in range(
        queue.size - pos
    ):  # (2n + 10) * (n - pos) =  2n^2 + 10n - 2n * pos - 10pos
        rotate(queue)

    return el


def pop_by_pos(queue: Queue[VT], pos: int) -> VT:  # 2n^2 + 10n + 6
    for _ in range(pos):  # (2n + 10)pos = 2n * pos + 10pos
        rotate(queue)

    el = queue.pop()  # 6

    for _ in range(
        queue.size - pos
    ):  # (2n + 10) * (n - pos) =  2n^2 + 10n - 2n * pos - 10pos
        rotate(queue)

    return el


def push_by_pos(queue: Queue[VT], el: VT, pos: int):  # 2n^2 + 8n - 4
    if pos >= queue.size:  # 2
        queue.push(el)  # 2n + 6
        return

    for _ in range(pos):  # 2n * pos + 10pos
        rotate(queue)

    queue.push(el)  # 6

    for _ in range(
        queue.size - pos - 1
    ):  # (2n + 10) * (n - pos - 1) =  2n^2 + 10n - 2n * pos - 10pos - 2n - 10
        rotate(queue)


def swap(queue: Queue, pos1: int, pos2: int):  # 8n^2 + 36n + 4
    temp = pop_by_pos(queue, pos1)  # 2n^2 + 10n + 6
    push_by_pos(
        queue, pop_by_pos(queue, pos2 - 1), pos1
    )  # 2n^2 + 8n - 4 + 2n^2 + 10n + 6
    push_by_pos(queue, temp, pos2)  # 2n^2 + 8n - 4


def heapify(queue: Queue, n: int, i: int):
    # (1 + 3 + 3 + 4n^2 + 20n + 5 + 1 + 4n^2 + 20n + 5 + 1 + 1 + 8n^2 + 36n + 4) * log(n * log(n)) =
    # = (16n^2 + 76n + 24) * log(n * log(n))
    largest = i  # 1
    l = 2 * i + 1  # 3
    r = 2 * i + 2  # 3

    if l < n and seek(queue, i) < seek(
        queue, l
    ):  # 1 + 1 + 2n^2 + 10n + 1 + 2n^2 + 10n + 2 = 4n^2 + 20n + 5
        largest = l  # 1

    if r < n and seek(queue, largest) < seek(
        queue, r
    ):  # 1 + 1 + 2n^2 + 10n + 1 + 2n^2 + 10n = 4n^2 + 20n + 5
        largest = r  # 1

    if largest != i:  # 1
        swap(queue, i, largest)  # 8n^2 + 36n + 4
        heapify(queue, n, largest)  # ~log(n * log(n))


def heap_sort(queue: Queue):
    # 1 + 8n^3 + 38n^2 + nlog(n * log(n)) / 2 + 12n + 24n^3 + 112n^2 + nlog(n * log(n)) + 28n =
    # 32n^3 * log(n * log(n)) + 150n^2 +  + 40n + 1
    n = queue.size  # 1

    for i in range(
        n // 2 - 1, -1, -1
    ):  # (n / 2) * (16n^2 + 76n + 24) * log(n * log(n)) ~= 8n^3 * log(n * log(n)) + 38n^2 + 12n
        heapify(queue, n, i)

    for i in range(n - 1, 0, -1):  # n * (
        swap(queue, 0, i)  # 8n^2 + 36n + 4
        heapify(queue, i, 0)  # (16n^2 + 76n + log(n*log(n)) + 24) * log(n * log(n))
    # ) ~= 24n^3 * log(n * log(n)) + 112n^2 + 28n


if __name__ == "__main__":
    import time
    from random import randint

    tests = 10
    step = 40

    for test_num in range(1, tests + 1):
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
