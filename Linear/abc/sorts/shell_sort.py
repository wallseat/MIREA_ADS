from Linear.abc.ICollection import Collection, seek, swap


# $DEF
def shell_sort(collection: Collection) -> Collection:  # $CX_PUSH: 1$
    last_index = collection.size - 1  # $CX_EXPR: 3$
    step = collection.size // 2  # $CX_EXPR: 3$
    while step > 0:  # $CX_PUSH: log(n)$
        for i in range(step, last_index + 1, 1):  # $CX_PUSH: n$
            j = i  # $CX_EXPR: 1$
            delta = j - step  # $CX_EXPR: 2$
            while delta >= 0 and seek(collection, delta) > seek(collection, j):  # $CX_PUSH: 1$
                # $CX_EXPR: seek + seek$
                swap(collection, delta, j)  # $CX_EXPR: swap$
                j = delta  # $CX_EXPR: 1$
                delta = j - step  # $CX_EXPR: 2$
            # ) = $CX_POP
        # ) = $CX_POP
        step //= 2  # $CX_EXPR: 2$
    # ) = $CX_POP

    return collection
    # $CX_POP_BACK


# $ENDEF
