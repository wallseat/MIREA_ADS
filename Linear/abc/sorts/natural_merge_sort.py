from Linear.abc.ICollection import VT, Collection, partition, pop_front, push_back, seek


# $DEF
def merge(left: Collection[VT], right: Collection[VT]) -> Collection[VT]:  # $CX_DEF $CX_PUSH: 1$
    result = Collection[VT]()  # $CX_EXPR: 1$

    while not left.empty and not right.empty:  # $CX_PUSH: n / 2$
        if seek(left, 0) <= seek(right, 0):  # $CX_EXPR: seek + seek + 1$
            push_back(result, pop_front(left))  # $CX_EXPR: push_back + pop_front$
        else:
            push_back(result, pop_front(right))  # $CX_EXPR: push_back + pop_front$
    # ) = $CX_POP

    while not left.empty:  # $CX_PUSH: 1$
        push_back(result, pop_front(left))  # $CX_EXPR: push_back + pop_front$
    # ) = $CX_POP

    while not right.empty:  # $CX_PUSH: 1$
        push_back(result, pop_front(right))  # $CX_EXPR: push_back + pop_front$
    # ) = $CX_POP

    return result

    # $CX_POP_BACK


def merge_sort(collection: Collection[VT]) -> Collection[VT]:  # $CX_PUSH: 1$
    if collection.size <= 1:  # $CX_EXPR: 2$
        return collection

    left = partition(collection, 0, collection.size // 2 - 1)  # $CX_EXPR: partition + 2$
    right = partition(collection, collection.size // 2)  # $CX_EXPR: partition + 1$

    left = merge_sort(left)  # $CX_EXPR: log(merge)$
    right = merge_sort(right)  # $CX_EXPR: log(merge)$

    result = merge(left, right)  # $CX_EXPR: merge$

    for _ in range(collection.size):  # $CX_PUSH: n$
        collection.pop()  # $CX_EXPR: Collection__pop$
    # ) = $CX_POP

    for _ in range(result.size):  # $CX_PUSH: n$
        push_back(collection, pop_front(result))  # $CX_EXPR: push_back + pop_front$
    # ) = $CX_POP

    collection._n_op += left.n_op + right.n_op

    return collection

    # $CX_POP_BACK


# $ENDEF
