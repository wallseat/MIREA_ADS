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


if __name__ == "__main__":
    from random import randint

    stack = Stack[int]()
    test_data = [randint(-100, 100) for _ in range(20)]

    for el in test_data:
        stack.push(el)

    print_stack(stack)

    # 1
    for i, el in enumerate(test_data):
        assert seek(stack, i) == el

    # 2
    test_data.insert(2, 20)
    push_by_pos(stack, 20, 2)

    for i, el in enumerate(test_data):
        assert seek(stack, i) == el

    # 3
    test_data.pop(2)
    pop_by_pos(stack, 2)
    for i, el in enumerate(test_data):
        assert seek(stack, i) == el

    # 4
    tmp = test_data[2]
    test_data[2] = test_data[5]
    test_data[5] = tmp

    swap(stack, 2, 5)
    for i, el in enumerate(test_data):
        assert seek(stack, i) == el

    # 5
    slice = slice_stack(stack, 5, 15)
    for i, el in enumerate(test_data[5:16]):
        assert seek(stack, i + 5) == el

    # 6
    for _ in test_data:
        stack.pop()

    assert stack.size == 0
    assert stack.is_empty() == True

    print("All tests passed")
