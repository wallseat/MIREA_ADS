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


def reverse(stack: Stack[VT]) -> Stack[VT]:  # 2n^2 + 2n + 1
    out = Stack[VT]()  # 1
    for _ in range(stack.size):  # n * (
        out.push(stack.pop())  # n + n + 2
    # ) = 2n^2 + 2n
    return out


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


def merge_sort(stack: Stack):  # 4(n^2)log(n) + 8n + 2log(nlog(n)) + 13
    def _merge(
        left: Stack, right: Stack
    ) -> Stack:  # 1 + 2 + k^3 + m^3 + k^3 + 2k + m^3 + 2m = 2k^3 + 2m^3 + 2k + 2m + 3
        result = Stack()  # 1
        i, j = 0, 0  # 2

        while i < left.size and j < right.size:  # ((k + m) / 2) * (
            left_v = seek(left, i)  # 2k^2 + 3k - 8
            right_v = seek(right, j)  # 2m^2 + 3m - 8

            if left_v < right_v:  # 1
                result.push(left_v)  # s + 2
                i += 1  # 1
            else:
                result.push(right_v)  # s + 2
                j += 1  # 1
        # ) ~= k^3 + m^3

        while i < left.size:  # (k / 2) * (
            result.push(seek(left, i))  # s + 2 + 2k^2
            i += 1  # 1
        # ) = sk / 2 + k + k^3 ~= k^3 + 2k

        while j < right.size:  # (m / 2) * (
            result.push(seek(right, j))  # s + 2 + 2m^2
            j += 1  # 1
        # ) = sm / 2 + m + m^3 ~= m^3 + 2m

        return result

    if stack.size < 2:  # 2
        return stack

    middle = stack.size // 2  # 3

    left_slice = slice_stack(stack, r=middle - 1)  # 2n^2 + 4n + 15
    right_slice = slice_stack(stack, l=middle)  # 2n^2 + 4n + 15 +
    left = merge_sort(left_slice)  # 2log(nlog(n))
    right = merge_sort(right_slice)  # 2log(nlog(n))
    sorted_stack = _merge(left, right)  # ~= (n^2)log(n)
    sorted_stack._n_op += left_slice.n_op + right_slice.n_op + left.n_op + right.n_op
    return sorted_stack


if __name__ == "__main__":
    import time
    from random import randint

    tests = 10
    step = 200

    for test_num in range(1, tests + 1):
        stack = Stack[int]()
        for _ in range(test_num * step):
            stack.push(randint(-10000, 10000))

        start_time = time.time()
        stack = merge_sort(stack)
        total_time = time.time() - start_time

        print(f"Test: {test_num}")
        print(f"Elems count: {test_num * step}")
        print(f"Total time: {total_time}")
        print(f"N_OP: {stack.n_op}")
        print("-------------")
