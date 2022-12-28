from ICollection import VT, Collection, pop_by_pos, push_by_pos, seek


# $DEF$
def binary_insertion_sort(collection: Collection[VT]) -> Collection[VT]:
    for i in range(1, collection.size):
        el = pop_by_pos(collection, i)
        l = 0
        r = i - 1
        while l <= r:
            mid = (l + r) // 2
            if el < seek(collection, mid):
                r = mid - 1
            else:
                l = mid + 1
        push_by_pos(collection, el, l)
    return collection


# $ENDEF$
