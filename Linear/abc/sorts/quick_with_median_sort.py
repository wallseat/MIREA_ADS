from Linear.abc.ICollection import Collection, seek, swap


# $DEF
def quick_sort(collection: Collection) -> Collection:  # $CX_PUSH: 1$
    def _quick_sort(left: int, right: int) -> None:  # $CX_PUSH: 1$
        i = left  # $CX_EXPR: 1$
        j = right  # $CX_EXPR: 1$

        partition_index = seek(collection, (i + j) // 2)  # $CX_EXPR: seek + 3$

        while i < j:  # $CX_PUSH: n$
            while seek(collection, i) < partition_index:  # $CX_PUSH: seek + 1$
                i += 1  # $CX_EXPR: 1$
            # )= $CX_POP
            while seek(collection, j) > partition_index:  # $CX_PUSH: seek + 1$
                j -= 1
            # )= $CX_POP

            if i <= j:  # $CX_EXPR: 1$
                if i < j:  # $CX_EXPR: 1$
                    swap(collection, i, j)  # $CX_EXPR: swap$
                i += 1  # $CX_EXPR: 1$
                j -= 1  # $CX_EXPR: 1$
        # ) = $CX_POP

        if left < j:  # $CX_EXPR: 1$
            _quick_sort(left, j)  # $CX_EXPR: log(n)$
        if i < right:  # 1
            _quick_sort(i, right)  # $CX_EXPR: log(n)$

        # $CX_POP_BACK

    _quick_sort(0, collection.size - 1)

    return collection
    # $CX_POP_BACK


# $ENDEF
