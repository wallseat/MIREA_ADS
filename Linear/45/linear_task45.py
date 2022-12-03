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
        self._nop += 1
        return len(self._queue) == 0

    @property
    def size(self) -> int:  # 1
        self._nop += 1
        return len(self._queue)

    @property
    def tail(self) -> VT:  # 1
        self._nop += 1
        return self._queue[-1]

    @property
    def head(self) -> VT:  # 1
        self._nop += 1
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


def slice_queue(
    queue: Queue[VT], l: int = 0, r: int = -1
) -> Queue[VT]:  # 1 + 1 + 3 + 2n + 4 + 2n + 6 + 2n^2 - 4 = 2n^2 + 4n + 15
    q = Queue[VT]()  # 1

    if r == -1:  # 1
        r = queue.size - 1  # 3

    for _ in range(l):  # l * (
        rotate(queue)  # 2n + 4
    # ) = 2ln + 4l ~= 2n + 4

    for _ in range(r - l + 1):  # (r - l + 1) * (
        q.push(queue.head)  # k + 2
        rotate(queue)  # 2n + 4
    # ) = (r - l + 1) * (k + 6 + 2n) = (rk - lk + k + 2rn - 2ln + 2n + 6r - 6l + 6) ~= 2n + 6

    for _ in range(queue.size - r - 1):  # (n - r - 1) * (
        rotate(queue)  # 2n + 4
    # ) = (2n^2 - 2rn - 2n + 4n - 4r - 4) ~= 2n^2 - 4
    return q


def merge_sort(queue: Queue):  # 4(n^2)log(n) + 8n + 2log(nlog(n)) + 13
    def _merge(
        left: Queue, right: Queue
    ) -> Queue:  # 1 + 2 + k^3 + m^3 + k^3 + 2k + m^3 + 2m = 2k^3 + 2m^3 + 2k + 2m + 3
        result = Queue()  # 1
        i, j = 0, 0  # 2

        while i < left.size and j < right.size:  # ((k + m) / 2) * (
            left_v = seek(left, i)  # 2k^2
            right_v = seek(right, j)  # 2m^2

            if left_v < right_v:  # 1
                result.push(left_v)  # s + 2
                i += 1  # 1
            else:
                result.push(right_v)  # s + 2
                j += 1  # 1
        # ) = k^3 + km^2 + ks + 3k + mk^2 + m^3 + ms + 3m ~= k^3 + m^3

        while i < left.size:  # (k / 2) * (
            result.push(seek(left, i))  # s + 2 + 2k^2
            i += 1  # 1
        # ) = sk / 2 + k + k^3 ~= k^3 + 2k

        while j < right.size:  # (m / 2) * (
            result.push(seek(right, j))  # s + 2 + 2m^2
            j += 1  # 1
        # ) = sm / 2 + m + m^3 ~= m^3 + 2m

        return result

    if queue.size < 2:  # 2
        return queue

    middle = queue.size // 2  # 3

    left_slice = slice_queue(queue, r=middle - 1)  # 2n^2 + 4n + 15
    right_slice = slice_queue(queue, l=middle)  # 2n^2 + 4n + 15 +
    left = merge_sort(left_slice)  # 2log(nlog(n))
    right = merge_sort(right_slice)  # 2log(nlog(n))
    sorted_queue = _merge(left, right)  # ~= (n^2)log(n)
    sorted_queue._nop += left_slice.n_op + right_slice.n_op + left.n_op + right.n_op
    return sorted_queue


if __name__ == "__main__":
    import time
    from random import randint

    tests = 10
    step = 200

    for test_num in range(1, tests + 1):
        queue = Queue[int]()
        for _ in range(test_num * step):
            queue.push(randint(-10000, 10000))

        start_time = time.time()
        queue = merge_sort(queue)
        total_time = time.time() - start_time

        print(f"Test: {test_num}")
        print(f"Elems count: {test_num * step}")
        print(f"Total time: {total_time}")
        print(f"N_OP: {queue.n_op}")
        print("-------------")
