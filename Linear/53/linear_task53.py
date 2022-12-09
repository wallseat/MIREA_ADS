from typing import Generic, List, TypeVar

VT = TypeVar("VT")


class Queue(Generic[VT]):
    _queue: List[VT]
    _nop: int

    def __init__(self):
        self._queue = []
        self._nop = 0

    def push(self, value: VT):  # n + 2
        self._nop += self.size + 2

        self._queue = self._queue.copy()
        self._queue.append(0)
        # Имитация работы со списком как с массивом.
        # Создание массива на элемент больше и копирование элементов
        self._queue[-1] = value

    def pop(self) -> VT:  # n + 2
        self._nop += self.size + 2

        if self.is_empty():
            raise Exception("Can't pop from empty queue!")

        el = self._queue[0]
        self._queue = self._queue[1:]  # создание нового списка на элемент меньше

        return el

    def is_empty(self) -> bool:  # 1
        return len(self._queue) == 0

    @property
    def size(self) -> int:  # 1
        return len(self._queue)

    @property
    def tail(self) -> VT:  # 1
        return self._queue[-1]

    @property
    def head(self) -> VT:  # 1
        return self._queue[0]

    @property
    def n_op(self) -> int:
        return self._nop


def print_queue(queue: Queue):
    elems = []
    for _ in range(queue.size):
        el = queue.pop()
        elems.append(el)
        queue.push(el)

    print("Queue[" + ", ".join(map(str, elems)) + "]")


def rotate(queue: Queue):  # 2n + 4
    queue.push(queue.pop())


def seek(
    queue: Queue, pos: int
):  # 2n * pos + 4pos + 4n + 8 + 2n^2 + 8n - 2n * pos - 4pos - 2n - 4 = 2n^2
    for _ in range(pos):  # pos * (2n + 4) = 2n * pos + 4pos
        rotate(queue)

    el = queue.pop()  # n + 2
    queue.push(el)  # n + 2

    for _ in range(
        queue.size - pos - 1
    ):  # (n - pos - 1) * (2n + 4) = 2n^2 + 8n - 2n * pos - 4pos - 2n - 4
        rotate(queue)

    return el


def pop_by_pos(queue: Queue, pos: int):  # 2n^2 + 3n - 2
    for _ in range(pos):  # 2n * pos + 4pos
        rotate(queue)

    el = queue.pop()  # n + 2

    for _ in range(queue.size - pos):  # (n - pos - 1) * (2n + 4)
        rotate(queue)

    return el


def push_by_pos(queue: Queue, el, pos: int):  # 2n^2 + 3n - 2

    if pos >= queue.size:  # 1
        queue.push(el)  # n + 2
        return

    for _ in range(pos):  # 2n * pos + 4pos
        rotate(queue)

    queue.push(el)  # n + 2

    for _ in range(queue.size - pos - 1):  # (n - pos - 1) * (2n + 4)
        rotate(queue)


def swap(queue: Queue, pos1: int, pos2: int):  # 6n^2 + 9n - 7
    temp = pop_by_pos(queue, pos1)  # 2n^2 + 3n - 2
    push_by_pos(queue, pop_by_pos(queue, pos2 - 1), pos1)  # 2n^2 + 3n - 3
    push_by_pos(queue, temp, pos2)  # 2n^2 + 3n - 2


def heapify(queue: Queue, n: int, i: int):  #  14n^2 + nlog(n) + 9n + 9
    largest = i  # 1
    l = 2 * i + 1  # 3
    r = 2 * i + 2  # 3

    if l < n and seek(queue, i) < seek(queue, l):  # 4n^2 + 3
        largest = l  # 1

    if r < n and seek(queue, largest) < seek(queue, r):  # 4n^2 + 3
        largest = r  # 1

    if largest != i:  # 1
        swap(queue, i, largest)  # 6n^2 + 9n - 7
        heapify(queue, n, largest)  # ~= nlog(n)


def heap_sort(queue: Queue):  # 27n^3 + 2n^2 * log(n) + 23n^2 + 7n
    n = queue.size  # 1

    for i in range(n // 2 - 1, -1, -1):  # (n // 2) * (
        heapify(queue, n, i)  # 14n^2 + nlog(n) + 9n + 9
    # ) = 7n^3 + n^2log(n) + 5n^2 + 5n

    for i in range(n - 1, 0, -1):  # n * (
        swap(queue, 0, i)  #  6n^2 + 9n - 7
        heapify(queue, i, 0)  # 14n^2 + nlog(n) + 9n + 9
    # ) = 20n^3 + n^2log(n) + 18n^2 + 2n


if __name__ == "__main__":
    import time
    from random import randint

    tests = 10
    step = 30

    for test_num in range(1, tests + 1):
        queue = Queue[int]()
        for _ in range(test_num * step):
            queue.push(randint(-10000, 10000))

        start_time = time.time()
        heap_sort(queue)
        total_time = time.time() - start_time

        print(f"Test: {test_num}")
        print(f"Elems count: {test_num * step}")
        print(f"Total time: {total_time}".replace(".", ","))
        print(f"N_OP: {queue.n_op}")
        print("-------------")
