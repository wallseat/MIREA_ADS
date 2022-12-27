from ICollection import VT, Collection, seek, swap


# $DEF$
def shell_sort(collection: Collection[VT]) -> Collection[VT]:
    last_index = collection.size - 1
    step = collection.size // 2
    while step > 0:  # log(n) * (
        for i in range(step, last_index + 1, 1):  # n * (
            j = i  # 1
            delta = j - step  # 2
            while delta >= 0 and seek(collection, delta) > seek(collection, j):
                swap(collection, delta, j)
                j = delta  # 1
                delta = j - step  # 2
            # ) =
        step //= 2
    # ) =

    return collection


# $ENDEF$
