from Linear.abc.ICollection import Collection, seek, swap


# $DEF
def simple_insertion_sort(collection: Collection) -> Collection:  # $CX_PUSH: 1$
    for i in range(1, collection.size):  # $CX_PUSH: n$
        for j in range(i, 0, -1):  # $CX_PUSH: n$
            if seek(collection, j - 1) > seek(collection, j):  # $CX_EXPR: seek + seek + 2$
                swap(collection, j - 1, j)  # $CX_EXPR: swap + 1$
            else:
                break
        # ) = $CX_POP
    # ) = $CX_POP

    return collection
    # ) = $CX_POP_BACK


# $ENDEF
