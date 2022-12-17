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


def merge(queue1: Queue[VT], queue2: Queue[VT]) -> Queue[VT]:  # 8n^2 + 8n + 1
    out = Queue[VT]()  # 1

    while queue1.size > 0 and queue2.size > 0:  # n * (
        if seek(queue1, 0) < seek(queue2, 0):  # 8n + 2
            out.push(queue1.pop())  # 2
        else:  # 1
            out.push(queue2.pop())  # 2
    # ) = 8n^2 + 4n

    while queue1.size > 0:  # n * (
        out.push(queue1.pop())  # 2
    # ) = 2n

    while queue2.size > 0:  # n * (
        out.push(queue2.pop())  # 2
    # ) = 2n

    out._n_op += queue1.n_op + queue2.n_op

    return out


def fixed_two_way_merge_sort(
    stack: Queue[VT],
) -> Queue[VT]:  # 8n^2 + 2n * log(n) + 12n + 8
    if stack.size <= 1:  # 2
        return stack

    stack_size = stack.size  # 2
    left_stack = Queue[VT]()  # 2
    right_stack = Queue[VT]()  # 2

    for _ in range(stack_size // 2):  # (n / 2) * (
        left_stack.push(stack.pop())  # 12
    # ) = n

    for _ in range(stack_size - stack_size // 2):  # (n / 2) * (
        right_stack.push(stack.pop())  # 2
    # ) = n

    left_stack = fixed_two_way_merge_sort(left_stack)  # ~= nlog(n)
    right_stack = fixed_two_way_merge_sort(right_stack)  # ~= nlog(n)

    buff = merge(left_stack, right_stack)  # 8n^2 + 8n + 1

    for _ in range(buff.size):  # n * (
        stack.push(buff.pop())  # 2
    # ) = 2n

    stack._n_op += buff.n_op

    return stack


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

        fixed_two_way_merge_sort(struct)
        print_queue(struct)

    elif sys.argv[1] == "tests":
        tests = 10
        step = 1000

        for test_num in range(1, tests + 1):
            struct = Queue[int]()

            for _ in range(test_num * step):
                struct.push(randint(-10000, 10000))

            start_time = time.time()
            fixed_two_way_merge_sort(struct)
            total_time = time.time() - start_time

            print(f"Test: {test_num}")
            print(f"Elements count: {test_num * step}")
            print(f"Total time: {total_time}".replace(".", ","))
            print(f"N_OP: {struct.n_op}")
            print("-------------")
