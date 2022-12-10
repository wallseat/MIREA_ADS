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


class Stack(Generic[VT]):
    _top: Optional[Node[VT]]
    _size: int
    _n_op: int

    def __init__(self) -> None:
        self._top = None
        self._size = 0
        self._n_op = 0

    def push(self, value: VT) -> None:  # 14
        node = Node(value)  # 2

        if self.is_empty():  # 2
            self._top = node  # 3
        else:
            node.next = self._top  # 3
            self._top = node  # 2

        self._size += 1  # 2
        self._n_op += 14

    def pop(self) -> VT:  # 9
        if self.is_empty():  # 2
            raise Exception("Can't pop from empty stack!")

        node = self._top  # 2
        self._top = node.next  # 3

        self._size -= 1  # 2
        self._n_op += 9

        return node.value

    def is_empty(self) -> bool:  # 2
        return self._size == 0

    @property
    def top(self) -> VT:  # 2
        return self._top.value

    @property
    def size(self) -> int:  # 1
        return self._size

    @property
    def n_op(self) -> int:
        return self._n_op


def print_stack(stack: Stack[VT]) -> None:
    buffer = Stack[VT]()

    elems = []
    for _ in range(stack.size):
        el = stack.pop()
        elems.append(el)
        buffer.push(el)

    print("Stack[" + ", ".join(map(str, elems)) + "]")

    for _ in range(buffer.size):
        el = buffer.pop()
        stack.push(el)


def seek(stack: Stack[VT], pos: int) -> VT:  # 46n - 40
    swap_stack = Stack[VT]()  # 2
    stack_size = stack.size  # 2

    for _ in range(stack_size - pos - 1):  # (n - 1) * (
        swap_stack.push(stack.pop())  # 23
    # ) = 23n - 23

    el = stack.top  # 2

    for _ in range(stack_size - pos - 1):  # (n - 1) * (
        stack.push(swap_stack.pop())  # 23
    # ) = 23n - 23

    return el


def push_by_pos(stack: Stack[VT], el: VT, pos: int) -> None:  # 46n - 28
    swap_stack = Stack()  # 2
    stack_size = stack.size  # 2

    for _ in range(stack_size - pos):  # n * (
        swap_stack.push(stack.pop())  # 23
    # ) = 23n - 23

    stack.push(el)  # 14

    for _ in range(stack_size - pos):  # n * (
        stack.push(swap_stack.pop())  # 23
    # ) = 23n - 23


def pop_by_pos(stack: Stack[VT], pos: int) -> VT:  # ~= 46n - 40
    swap_stack = Stack()
    stack_size = stack.size

    for _ in range(stack_size - pos - 1):
        swap_stack.push(stack.pop())

    el = stack.pop()

    for _ in range(stack_size - pos - 1):
        stack.push(swap_stack.pop())

    return el


def swap(stack: Stack[VT], pos1: int, pos2: int) -> None:  # 138n - 96
    temp = pop_by_pos(stack, pos1)  # 46n - 40
    push_by_pos(stack, pop_by_pos(stack, pos2 - 1), pos1)  # 46n - 28
    push_by_pos(stack, temp, pos2)  # 46n - 28


def reverse(stack: Stack[VT]) -> Stack[VT]:  # 23n
    out = Stack[VT]()  # 2
    for _ in range(stack.size):  # n * (
        out.push(stack.pop())  # 23
    # ) = 23n
    return out


def slice_stack(stack: Stack[VT], l: int = 0, r: int = -1) -> Stack[VT]:  # 83n - 49
    stack_size = stack.size  # 2
    slice_stack = Stack[VT]()  # 2
    swap_stack = Stack[VT]()  # 2

    if r == -1:  # 2
        r = stack.size - 1  # 3

    for _ in range(stack_size - r - 1):  # (n - 1) * (
        swap_stack.push(stack.pop())  # 23
    # ) = 23n - 23

    for _ in range(r - l + 1):  # (n - 1) * (
        slice_stack.push(stack.top)  # 14
        swap_stack.push(stack.pop())  # 23
    # ) = 37n - 37

    for _ in range(swap_stack.size):  # n * (
        stack.push(swap_stack.pop())  # 23
    # ) = 23n

    return reverse(slice_stack)  # 23n


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
