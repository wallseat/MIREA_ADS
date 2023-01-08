from numbers import Real


class Collection:
    _n_op: int

    def push(self, value: Real) -> None:  # Не гарантирует порядок
        ...

    def pop(self) -> Real:  # Не гарантирует порядок
        ...

    @property
    def size(self) -> int:
        ...

    @property
    def empty(self) -> bool:
        ...

    @property
    def n_op(self) -> int:
        ...


def pop_by_pos(collection: Collection, pos: int) -> Real:
    ...


def push_by_pos(collection: Collection, el: Real, pos: int) -> None:
    ...


def swap(collection: Collection, pos1: int, pos2: int) -> None:
    ...


def seek(collection: Collection, i: int) -> Real:
    ...


def push_front(collection: Collection, el: Real) -> None:
    ...


def pop_front(collection: Collection) -> Real:
    ...


def push_back(collection: Collection, el: Real) -> None:
    ...


def pop_back(collection: Collection) -> Real:
    ...


def partition(collection: Collection, l: int, r: int) -> Collection:
    ...
