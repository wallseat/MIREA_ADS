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

    def __init__(self) -> None:
        self._head = None
        self._size = 0
        self._n_op = 0

    def push(self, value: VT) -> None:  # 2n + 9
        node = Node(value)  # 2

        if self.is_empty():  # 1
            self._head = node  # 1
        else:
            if self._head.next != None:
                tail = self._head.next  # 3
                while tail.next is not None:  # n * (
                    tail = tail.next  # 2
                # ) = 2n
            else:
                tail = self._head  # 2

            tail.next = node  # 2

        self._size += 1  # 1

        self._n_op += self._size * 2 + 8

    def pop(self) -> VT:  # 7
        if self.is_empty():  # 1
            raise Exception("Can't pop from empty queue!")

        node = self._head  # 1
        self._head = node.next  # 2

        self._size -= 1  # 1
        self._n_op += 7

        return node.value

    def is_empty(self) -> bool:  # 2
        return self._size == 0

    @property
    def head(self) -> VT:  # 2
        return self._head.value

    @property
    def size(self) -> int:  # 1
        return self._size

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


def rotate(queue: Queue[VT]) -> None:  # 2n + 16
    queue.push(queue.pop())  # 2n + 16


def seek(queue: Queue[VT], pos: int) -> VT:  # 4n^2 + 32n + 2
    for _ in range(pos):  # n * (
        rotate(queue)  # 2n + 16
    # ) = 2n^2 + 16n

    el = queue.head  # 2

    for _ in range(queue.size - pos):  # n * (
        rotate(queue)  # 2n + 16
    # ) = 2n^2 + 16n

    return el


def pop_by_pos(queue: Queue[VT], pos: int) -> VT:  # 4n^2 + 32n + 7
    for _ in range(pos):  # n * (
        rotate(queue)  # 2n + 16
    # ) = 2n^2 + 16n

    el = queue.pop()  # 7

    for _ in range(queue.size - pos):  # n * (
        rotate(queue)  # 2n + 16
    # ) = 2n^2 + 16n

    return el


def push_by_pos(queue: Queue[VT], el: VT, pos: int) -> None:  # 4n^2 + 34n + 11
    if pos >= queue.size:  # 2
        queue.push(el)  # 2n + 9
        return

    for _ in range(pos):  # n * (
        rotate(queue)  # 2n + 16
    # ) = 2n^2 + 16n

    queue.push(el)  # 2n + 9

    for _ in range(queue.size - pos - 1):  # n * (
        rotate(queue)  # 2n + 16
    # ) = 2n^2 + 16n


def swap(queue: Queue, pos1: int, pos2: int):  # 16n^2 + 132n + 36
    temp = pop_by_pos(queue, pos1)  # 4n^2 + 32n + 7
    push_by_pos(queue, pop_by_pos(queue, pos2 - 1), pos1)  # 8n^2 + 66n + 18
    push_by_pos(queue, temp, pos2)  # 4n^2 + 34n + 11


def slice_(queue: Queue[VT], l: int = 0, r: int = -1) -> Queue[VT]:  # 8n^2 + 57n + 6
    buffer = Queue[VT]()  # 2

    if r == -1:  # 1
        r = queue.size - 1  # 3

    for _ in range(l):  # n * (
        rotate(queue)  # 2n + 16
    # ) = 2n^2 + 16n

    for _ in range(r - l + 1):  # n * (
        el = queue.pop()  #  7

        buffer.push(el)  # 2n + 9

        queue.push(el)  # 2n + 9
    # ) = 4n^2 + 25n

    for _ in range(queue.size - r - 1):  # n * (
        rotate(queue)  # 2n + 16
    # ) = 2n^2 + 16n

    return buffer


def quick_sort(queue: Queue[VT]) -> Queue[VT]:  # 24n^3 + 200n^2 + 2nlog(n) + 74n + 2
    def _quick_sort(
        left: int, right: int
    ) -> None:  # 24n^3 + 200n^2 + 2nlog(n) + 74n + 2
        i = left  # 1
        j = right  # 1

        partition_index = seek(queue, (i + j) // 2)  # 4n^2 + 32n + 2

        while i < j:  # n * (
            while seek(queue, i) < partition_index:  # 4n^2 + 32n + 3
                i += 1
            while seek(queue, j) > partition_index:  # 4n^2 + 32n + 3
                j -= 1

            if i <= j:  # 1
                if i < j:  # 1
                    swap(queue, i, j)  # 16n^2 + 132n + 36
                i += 1  # 1
                j -= 1  # 1
        # ) = 24n^3 + 196n^2 + 42n

        if left < j:  # 1
            _quick_sort(left, j)  # ~= nlog(n)
        if i < right:  # 1
            _quick_sort(i, right)  # ~= nlog(n)

    _quick_sort(0, queue.size - 1)

    return queue


if __name__ == "__main__":
    import sys
    import time
    from random import randint

    if len(sys.argv) < 2 or sys.argv[1] not in ["example", "tests"]:
        print(f"Usage: python3 {sys.argv[0]} [example/tests]")
        exit(1)

    if sys.argv[1] == "example":
        struct = Queue[int]()
        for _ in range(20):
            struct.push(randint(-10000, 10000))

        quick_sort(struct)
        print_queue(struct)

    elif sys.argv[1] == "tests":
        tests = 10
        step = 60

        for test_num in range(1, tests + 1):
            struct = Queue[int]()

            for _ in range(test_num * step):
                struct.push(randint(-10000, 10000))

            start_time = time.time()
            quick_sort(struct)
            total_time = time.time() - start_time

            print(f"Test: {test_num}")
            print(f"Elements count: {test_num * step}")
            print(f"Total time: {total_time}")
            print(f"N_OP: {struct.n_op}")
            print("-------------")
