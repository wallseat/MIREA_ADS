from Linear.abc.ICollection import Collection, pop_by_pos, push_by_pos, seek


# $DEF
def binary_insertion_sort(collection: Collection) -> Collection:  # $CX_PUSH: 1$
    for i in range(1, collection.size):  # $CX_PUSH: n$
        el = pop_by_pos(collection, i)  # $CX_EXPR: pop_by_pos$
        l = 0  # $CX_EXPR: 1$
        r = i - 1  # $CX_EXPR: 2$
        while l <= r:  # $CX_PUSH: log(n)$
            mid = (l + r) // 2  # $CX_EXPR: 3$
            if el < seek(collection, mid):  # $CX_EXPR: seek + 1$
                r = mid - 1  # $CX_EXPR: 2$
            else:
                l = mid + 1
        # )= $CX_POP
        push_by_pos(collection, el, l)  # $CX_EXPR: push_by_pos$
    # )= $CX_POP
    return collection
    # $CX_POP_BACK


# $ENDEF
