from ICollection import VT, Collection, push_back, seek


# $DEF
def counting_sort(collection: Collection[VT]) -> Collection[VT]:  # $CX_PUSH
    max_ = seek(collection, 0) # $CX_EXPR: seek$
    min_ = max_ # $CX_EXPR: 1$

    buffer = Collection[VT]() # $CX_EXPR: 1$

    while not collection.empty:  # $CX_PUSH $CX_EXPR: n * ($
        el = collection.pop()  # $CX_EXPR: Collection__pop$
        if el > max_:  # $CX_EXPR: 1$
            max_ = el  # $CX_EXPR: 1$
        if el < min_:  # $CX_EXPR: 1$
            min_ = el  # $CX_EXPR: 1$
        buffer.push(el)  # $CX_EXPR: Collection__push$
    # $CX_EXPR: )$
    # )= $CX_POP

    counter = [0] * (max_ - min_ + 1)  # $CX_EXPR: 1 $

    while not buffer.empty:  # $CX_PUSH $CX_EXPR: n * ($
        el = buffer.pop()  # $CX_EXPR: Collection__pop + 1$
        counter[el - min_] += 1  # $CX_EXPR: 3 $
    # $CX_EXPR: )$ )= $CX_POP

    for i, count in enumerate(counter):  # $CX_PUSH $CX_EXPR: n * ($
        if count:  # $CX_EXPR: 1$
            for _ in range(count):  # $CX_PUSH $CX_EXPR: 1 * ($
                push_back(collection, i + min_)  # $CX_EXPR: push_back$
            # $CX_EXPR: )$ )= $CX_POP
    # $CX_EXPR: )$ )= $CX_POP

    return collection
    # $CX_POP_BACK


# $ENDEF
