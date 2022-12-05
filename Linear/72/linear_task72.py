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


def simple_choice_sort(
    stack: Stack,
) -> Stack:
    #  1 + n + log(n)*4n^3 + log(n)*6n^2 - log(n)*16n - log(n)*4n^2 - log(n)*6n + log(n)16 + log(n)n - n + 8n^3 + 14n^2 - 12n =
    # = 4log(n)n^3 + 8n^3 + 2log(n)n^2 + 14n^2 - 22log(n)n - 12n + 16log(n) + 1
    """Sorts a list of integers in ascending order using the selection sort algorithm."""
    n = stack.size  # 1
    for i in range(n):  # n * (
        min_index = i  # 1
        for j in range(i + 1, n):  # (n - i - 1) ~= log(n) * (
            if seek(stack, j) < seek(stack, min_index):  # 4n^2 + 6n - 16
                min_index = j  # 1
        swap(stack, i, min_index)  # 8n^2 + 14n - 12

    return stack


if __name__ == "__main__":
    import time
    from random import randint

    tests = 10
    step = 50

    for test_num in range(1, tests + 1):
        stack = Stack[int]()
        for _ in range(test_num * step):
            stack.push(randint(-10000, 10000))

        start_time = time.time()
        stack = simple_choice_sort(stack)
        total_time = time.time() - start_time

        print(f"Test: {test_num}")
        print(f"Elems count: {test_num * step}")
        print(f"Total time: {total_time}")
        print(f"N_OP: {stack.n_op}")
        print("-------------")
