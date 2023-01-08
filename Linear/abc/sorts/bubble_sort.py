from Linear.abc.ICollection import Collection, seek, swap


# $DEF
def bubble_sort(collection: Collection) -> Collection:  # $CX_PUSH: 1$
    for i in range(collection.size):  # $CX_PUSH: n$
        for j in range(i, collection.size):  # $CX_PUSH: (n - 1) / 3$
            if seek(collection, i) > seek(collection, j):  # $CX_EXPR: seek + seek + 1$
                swap(collection, i, j)  # $CX_EXPR: swap$
        # )= $CX_POP
    # )= $CX_POP
    return collection
    # $CX_POP_BACK


# $ENDEF
