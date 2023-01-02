from Linear.abc.ICollection import VT, Collection, seek, swap


# $DEF
def selection_sort(collection: Collection[VT]) -> Collection[VT]:  # $CX_PUSH: 1$
    for start_pos in range(collection.size):  # $CX_PUSH: n$
        min_el_pos = start_pos  # 1
        min_el = seek(collection, min_el_pos)  # $CX_EXPR: seek + 1$

        for check_el_pos in range(start_pos + 1, collection.size):  # $CX_PUSH: n$
            check_el = seek(collection, check_el_pos)  # $CX_EXPR: seek + 1$
            if check_el < min_el:  # $CX_EXPR: 1$
                min_el = check_el  # $CX_EXPR: 1$
                min_el_pos = check_el_pos  # $CX_EXPR: 1$
        # ) = $CX_POP

        if min_el_pos != start_pos:  # $CX_EXPR: 1$
            swap(collection, start_pos, min_el_pos)  # $CX_EXPR: swap$
    # ) = $CX_POP
    # $CX_POP_BACK


# $ENDEF
