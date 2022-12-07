from typing import Generic, List, TypeVar

VT = TypeVar("VT")


class Stack(Generic[VT]):
    _stack: List[VT]
    _n_op: int

    def __init__(self):
        self._stack = []
        self._n_op = 0

    def push(self, el: VT):  # n + 2
        self._n_op += self.size + 2

        self._stack = self._stack.copy()
        self._stack.append(el)

    def pop(self) -> VT:  # n + 2
        self._n_op += self.size + 2

        if self.is_empty():
            raise Exception("Can't pop from empty stack!")

        el = self._stack[-1]
        self._stack = self._stack[:-1]

        return el

    def is_empty(self):  # 1
        return len(self._stack) == 0

    @property
    def n_op(self):
        return self._n_op

    @property
    def size(self):  # 1
        return len(self._stack)

    @property
    def top(self):  # 1
        return self._stack[-1]

    def __str__(self) -> str:
        return "Stack[" + ", ".join(map(str, self._stack)) + "]"


def print_stack(stack: Stack):
    print("Stack[" + ", ".join(map(str, stack._stack)) + "]")


def seek(stack: Stack, pos: int):  # ~= 2n^2 + 3n - 8
    swap_stack = Stack()  # 1
    stack_size = stack.size  # 2

    for _ in range(stack_size - pos - 1):  # (n - pos - 1) * (
        swap_stack.push(stack.pop())  # k + 2 + n + 2
    # ) ~= n^2 + 4n - n*pos - 4pos - n - 4

    el = stack.top  # 2

    for _ in range(stack_size - pos - 1):  # (n - pos - 1) * (
        stack.push(swap_stack.pop())  # k + 2 + n + 2
    # ) ~= n^2 + 4n - n*pos - 4pos - n - 4

    return el


def push_by_pos(stack: Stack[VT], el: VT, pos: int):  # ~= 2n^2 + 4n + 2
    swap_stack = Stack()  # 1
    stack_size = stack.size  # 2

    for _ in range(stack_size - pos):  # (n - pos) * (
        swap_stack.push(stack.pop())  # k + n + 4
    # ) ~= n^2 + 4n - n * pos - 4pos

    stack.push(el)  # n + 2

    for _ in range(stack_size - pos):  # (n - pos) * (
        stack.push(swap_stack.pop())  # k + n + 4
    # ) ~= n^2 + 4n - n * pos - 4pos


def pop_by_pos(stack: Stack[VT], pos: int) -> VT:  # ~= 2n^2 + 3n - 8
    swap_stack = Stack()  # 1
    stack_size = stack.size  # 2

    for _ in range(stack_size - pos - 1):  # (n - pos - 1) * (
        swap_stack.push(stack.pop())  # k + 2 + n + 2
    # ) ~= n^2 + 4n - n*pos - 4pos - n - 4

    el = stack.pop()  # n + 2

    for _ in range(stack_size - pos - 1):  # (n - pos - 1) * (
        stack.push(swap_stack.pop())  # k + 2 + n + 2
    # ) ~= n^2 + 4n - n*pos - 4pos - n - 4

    return el


def swap(stack: Stack, pos1: int, pos2: int):  # 8n^2 + 14n - 12
    temp = pop_by_pos(stack, pos1)  # 2n^2 + 3n - 8
    push_by_pos(
        stack, pop_by_pos(stack, pos2 - 1), pos1
    )  # 2n^2 + 4n + 2 + 2n^2 + 3n - 8
    push_by_pos(stack, temp, pos2)  # 2n^2 + 4n + 2


def slice_stack(
    stack: Stack[VT], l: int = 0, r: int = -1
) -> Stack[VT]:  # 4 + 4 + n^2 + 3n - 5 + n + n^2 + 2n = 2n^2 + 6n + 3
    stack_size = stack.size  # 2
    slice_stack = Stack[VT]()  # 1
    swap_stack = Stack[VT]()  # 1

    if r == -1:  # 1
        r = stack.size - 1  # 3

    for _ in range(stack_size - r - 1):  # (n - r - 1) * (
        swap_stack.push(stack.pop())  # k + n + 4
    # ) ~= n^2 + 3n - 5

    for _ in range(r - l + 1):  # (r - l + 1) * (
        slice_stack.push(stack.top)  # k + 3
        swap_stack.push(stack.pop())  # s + n + 4
    # ) ~= n

    for _ in range(swap_stack.size):  # n * (
        stack.push(swap_stack.pop())  # k + n + 2
    # ) ~= n^2 + 2n

    return reverse(slice_stack)  # 2n^2 + 2n + 1


def reverse(stack: Stack[VT]) -> Stack[VT]:  # 2n^2 + 2n + 1
    out = Stack[VT]()  # 1
    for _ in range(stack.size):  # n * (
        out.push(stack.pop())  # n + n + 2
    # ) = 2n^2 + 2n
    return out


def merge(stack1: Stack[VT], stack2: Stack[VT]) -> Stack[VT]:
    out = Stack[VT]()  # 1

    while stack1.size > 0 and stack2.size > 0:  # n * (
        if stack1.top > stack2.top:  # 3
            out.push(stack1.pop())  # n + n + 3
        else:  # 1
            out.push(stack2.pop())  # n + n + 3
    # ) = 4n^2 + 6n

    while stack2.size > 0:  # n * (
        out.push(stack2.pop())  # n + n + 3
    # ) = 2n^2 + 3n

    while stack1.size > 0:  # n * (
        out.push(stack1.pop())  # n + n + 3
    # ) = 2n^2 + 3n

    return reverse(out)  # 1


def fixed_two_way_merge_sort(
    stack: Stack[VT],
) -> Stack[VT]:  # ~= 6n^2 * log(n) + 6n * log(n) + 3log(n)
    if stack.size <= 1:  # 1
        return stack  # 1

    stack_size = stack.size  # 2
    left_stack = Stack[VT]()  # 1
    right_stack = Stack[VT]()  # 1

    for _ in range(stack_size // 2):  # (n // 2) * (
        left_stack.push(stack.pop())  # 2n + 4
    # ) ~= n^2 + 2n

    for _ in range(stack_size - stack_size // 2):  # (n - n // 2) * (
        right_stack.push(stack.pop())  # 2n + 4
    # ) ~= n^2 + 2n

    left_stack = fixed_two_way_merge_sort(left_stack)  # 2n^2 + 2n + 1
    right_stack = fixed_two_way_merge_sort(right_stack)  # 2n^2 + 2n + 1

    return merge(left_stack, right_stack)  # 2n^2 + 2n + 1


if __name__ == "__main__":
    import time
    from random import randint

    tests = 10
    step = 5000

    for test_num in range(1, tests + 1):
        stack = Stack[int]()
        for _ in range(test_num * step):
            stack.push(randint(-10000, 10000))

        start_time = time.time()
        fixed_two_way_merge_sort(stack)
        total_time = time.time() - start_time

        print(f"Test: {test_num}")
        print(f"Elems count: {test_num * step}")
        print(f"Total time: {total_time}")
        print(f"N_OP: {stack.n_op}")
        print("-------------")
