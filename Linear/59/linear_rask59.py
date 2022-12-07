from typing import Generic, Optional, TypeVar

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


def simple_insertion_sort(queue: Queue[VT]) -> Queue[VT]:
    for i in range(1, queue.size):  # n * (
        for j in range(i, 0, -1):  # n * (
            if seek(queue, j - 1) > seek(queue, j):  # 4n^2 + 20n + 6
                swap(queue, j - 1, j)  # 8n^2 + 36n + 5
            else:
                break
        # ) = 12n^3 + 56n^2 + 11n
    # ) = 12n^4 + 56n^3 + 11n^2

    return queue


if __name__ == "__main__":
    import time
    from random import randint

    tests = 10
    step = 10

    for test_num in range(1, tests + 1):
        queue = Queue[int]()
        for _ in range(test_num * step):
            queue.push(randint(-10000, 10000))

        start_time = time.time()
        simple_insertion_sort(queue)
        total_time = time.time() - start_time

        print(f"Test: {test_num}")
        print(f"Elems count: {test_num * step}")
        print(f"Total time: {total_time}".replace(".", ","))
        print(f"N_OP: {queue.n_op}")
        print("-------------")
