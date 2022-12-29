from typing import Generic, TypeVar
from numbers import Real


VT = TypeVar("VT", bound=Real)


class Collection(Generic[VT]):
    _n_op: int

    def push(self, value: VT) -> None:  # Не гарантирует порядок
        ...

    def pop(self) -> VT:  # Не гарантирует порядок
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


def pop_by_pos(collection: Collection[VT], pos: int) -> VT:
    ...


def push_by_pos(collection: Collection[VT], el: VT, pos: int) -> None:
    ...


def swap(collection: Collection[VT], pos1: int, pos2: int) -> None:
    ...


def seek(collection: Collection[VT], i: int) -> VT:
    ...


def push_front(collection: Collection[VT], el: VT) -> None:
    ...


def pop_front(collection: Collection[VT]) -> VT:
    ...


def push_back(collection: Collection[VT], el: VT) -> None:
    ...


def pop_back(collection: Collection[VT]) -> VT:
    ...


def slice_(collection: Collection[VT], l: int, r: int) -> Collection[VT]:
    ...
