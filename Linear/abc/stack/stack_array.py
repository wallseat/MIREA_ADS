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


def print_stack(stack: Stack[VT]) -> None:
    buffer = Stack[VT](max_size=stack.size)

    elements = []
    for _ in range(stack.size):
        el = stack.pop()
        elements.append(el)
        buffer.push(el)

    print("Stack[" + ", ".join(map(str, elements)) + "]")

    for _ in range(buffer.size):
        stack.push(buffer.pop())


def seek(stack: Stack[VT], pos: int) -> VT:  # 28n - 22
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


def push_by_pos(stack: Stack[VT], el: VT, pos: int) -> None:  # 28n + 9
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


def swap(stack: Stack[VT], pos1: int, pos2: int) -> None:  # 112n - 12
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


def slice_(stack: Stack[VT], l: int = 0, r: int = -1) -> Stack[VT]:  # 62n + 18
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
    slice = slice_(stack, 5, 15)
    for i, el in enumerate(test_data[5:16]):
        assert seek(stack, i + 5) == el

    # 6
    for _ in test_data:
        stack.pop()

    assert stack.size == 0
    assert stack.is_empty() == True

    print("All tests passed")
