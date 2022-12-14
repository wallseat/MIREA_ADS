from typing import Generic, List, TypeVar

VT = TypeVar("VT")


class Stack(Generic[VT]):
    _stack: List[VT]
    _size: int
    _n_op: int

    def __init__(self, max_size: int = 10000):
        self._stack = [None for _ in range(max_size)]
        self._n_op = 0
        self._size = 0

    def push(self, el: VT):  # 5
        self._stack[self.size] = el  # 3
        self._size += 1  # 2

        self._n_op += 5

    def pop(self) -> VT:  # 9
        if self.is_empty():  # 2
            raise Exception("Can't pop from empty stack!")

        el = self._stack[self._size - 1]  #  5
        self._size -= 1  # 2

        self._n_op += 9

        return el

    def is_empty(self) -> bool:  # 2
        return self._size == 0

    @property
    def n_op(self) -> int:
        return self._n_op

    @property
    def size(self) -> int:  # 1
        return self._size

    @property
    def top(self) -> VT:  # 1
        return self._stack[self._size - 1]


def print_stack(stack: Stack[VT]):
    buffer = Stack[VT](max_size=stack.size)

    elements = []
    for _ in range(stack.size):
        el = stack.pop()
        elements.append(el)
        buffer.push(el)

    print("Stack[" + ", ".join(map(str, elements)) + "]")

    for _ in range(buffer.size):
        stack.push(buffer.pop())


def seek(stack: Stack[VT], pos: int):  # 28n - 22
    buffer = Stack[VT](max_size=stack.size)  # 2
    stack_size = stack.size  # 2

    for _ in range(stack_size - pos - 1):  # (n - 1) * (
        buffer.push(stack.pop())  # 14
    # ) = 14n - 14

    el = stack.top  # 2

    for _ in range(stack_size - pos - 1):  # (n - 1) * (
        stack.push(buffer.pop())  # 14
    # ) = 14n - 14

    stack._n_op += buffer.n_op

    return el


def push_by_pos(stack: Stack[VT], el: VT, pos: int):  # 28n + 9
    buffer = Stack[VT](max_size=stack.size)  # 2
    stack_size = stack.size  # 2

    for _ in range(stack_size - pos):  # n * (
        buffer.push(stack.pop())  # 14
    # ) = 14n

    stack.push(el)  # 5

    for _ in range(stack_size - pos):  # n * (
        stack.push(buffer.pop())  # 14
    # ) = 14n

    stack._n_op += buffer.n_op


def pop_by_pos(stack: Stack[VT], pos: int) -> VT:  # 28n - 15
    buffer = Stack[VT](max_size=stack.size)  # 2
    stack_size = stack.size  # 2

    for _ in range(stack_size - pos - 1):  # (n - 1) * (
        buffer.push(stack.pop())  # 14
    # )= 14n - 14

    el = stack.pop()  # 9

    for _ in range(stack_size - pos - 1):  # (n - 1) * (
        stack.push(buffer.pop())  # 14
    # ) = 14n - 14

    stack._n_op += buffer.n_op

    return el


def swap(stack: Stack, pos1: int, pos2: int):  # 112n - 12
    temp = pop_by_pos(stack, pos1)  #  28n - 15
    push_by_pos(stack, pop_by_pos(stack, pos2 - 1), pos1)  # 56n - 6
    push_by_pos(stack, temp, pos2)  # 28n + 9


def reverse(stack: Stack[VT]) -> Stack[VT]:  # 14n + 2
    out = Stack[VT](max_size=stack.size)  # 2
    for _ in range(stack.size):  # n * (
        out.push(stack.pop())  # 14
    # ) = 14n

    out._n_op += stack.n_op
    return out


def slice_stack(stack: Stack[VT], l: int = 0, r: int = -1) -> Stack[VT]:  # 62n + 18
    stack_size = stack.size  # 2
    slice_stack = Stack[VT](max_size=stack.size)  # 2
    buffer = Stack[VT](max_size=stack.size)  # 2

    if r == -1:  # 1
        r = stack.size - 1  # 3

    for _ in range(stack_size - r - 1):  # (n - 1) * (
        buffer.push(stack.pop())  # 14
    # ) = 14n - 14

    for _ in range(r - l + 1):  # (n + 1) * (
        slice_stack.push(stack.top)  # 6
        buffer.push(stack.pop())  # 14
    # ) = 20n + 20

    for _ in range(buffer.size):  # n * (
        stack.push(buffer.pop())  # 14
    # ) = 14n

    slice_stack._n_op += buffer.n_op
    slice_stack._n_op += stack.n_op

    return reverse(slice_stack)  # 14n + 2


def merge(stack1: Stack[VT], stack2: Stack[VT]) -> Stack[VT]:  # 74n + 3
    out = Stack[VT](max_size=stack1.size + stack2.size)  # 1

    while stack1.size > 0 and stack2.size > 0:  # n * (
        if stack1.top < stack2.top:  # 3
            out.push(stack1.pop())  # 14
        else:  # 1
            out.push(stack2.pop())  # 14
    # ) = 32n

    while stack1.size > 0:  # n * (
        out.push(stack1.pop())  # 14
    # ) = 14n

    while stack2.size > 0:  # n * (
        out.push(stack2.pop())  # 14
    # ) = 14n

    out._n_op += stack1.n_op + stack2.n_op

    return reverse(out)  # 14n + 2


def fixed_two_way_merge_sort(stack: Stack[VT]) -> Stack[VT]:  # 2n * log(n) + 116n + 13
    if stack.size <= 1:  # 1
        return stack  # 1

    stack_size = stack.size  # 2
    left_stack = Stack[VT](max_size=stack.size)  # 2
    right_stack = Stack[VT](max_size=stack.size)  # 2

    for _ in range(stack_size // 2):  # (n / 2) * (
        left_stack.push(stack.pop())  # 14
    # ) = 7n

    for _ in range(stack_size - stack_size // 2):  # (n / 2) * (
        right_stack.push(stack.pop())  # 14
    # ) = 7n

    left_stack = fixed_two_way_merge_sort(left_stack)  # ~= nlog(n)
    right_stack = fixed_two_way_merge_sort(right_stack)  # ~= nlog(n)

    buff = reverse(merge(left_stack, right_stack))  # 88n + 5

    for _ in range(buff.size):  # n * (
        stack.push(buff.pop())  # 14
    # ) = 14n

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
        struct = Stack[int]()
        for _ in range(20):
            struct.push(randint(-10000, 10000))

        fixed_two_way_merge_sort(struct)
        print_stack(struct)

    elif sys.argv[1] == "tests":
        tests = 10
        step = 5000

        for test_num in range(1, tests + 1):
            struct = Stack[int](max_size=test_num * step)

            for _ in range(test_num * step):
                struct.push(randint(-10000, 10000))

            start_time = time.time()
            fixed_two_way_merge_sort(struct)
            total_time = time.time() - start_time

            print(f"Test: {test_num}")
            print(f"Elements count: {test_num * step}")
            print(f"Total time: {total_time}")
            print(f"N_OP: {struct.n_op}")
            print("-------------")
