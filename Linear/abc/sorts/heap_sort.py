from Linear.abc.ICollection import VT, Collection, seek, swap


# $DEF
def heapify(collection: Collection[VT], n: int, i: int) -> None:  # $CX_DEF $CX_PUSH: 1$
    largest = i  # $CX_EXPR: 1$
    l = 2 * i + 1  # $CX_EXPR: 3$
    r = 2 * i + 2  # $CX_EXPR: 3$

    if l < n and seek(collection, i) < seek(collection, l):  # $CX_EXPR: seek + seek + 3$
        largest = l  # $CX_EXPR: 1$

    if r < n and seek(collection, largest) < seek(collection, r):  # $CX_EXPR: seek + seek + 3$
        largest = r  # $CX_EXPR: 1$

    if largest != i:  # $CX_EXPR: 1$
        swap(collection, i, largest)  # $CX_EXPR: swap$
        heapify(collection, n, largest)  # $CX_EXPR: log(n)$
    # $CX_POP_BACK


def heap_sort(collection: Collection[VT]) -> Collection[VT]:  # $CX_PUSH: 1$
    n = collection.size  # $CX_EXPR: 1$

    for i in range(n // 2 - 1, -1, -1):  # $CX_PUSH: n / 2$
        heapify(collection, n, i)  # $CX_EXPR: heapify$
    # ) = $CX_POP

    for i in range(n - 1, 0, -1):  # $CX_PUSH: n$
        swap(collection, 0, i)  # $CX_EXPR: swap$
        heapify(collection, i, 0)  # $CX_EXPR: heapify$
    # ) = $CX_POP

    # $CX_POP_BACK


# $ENDEF
