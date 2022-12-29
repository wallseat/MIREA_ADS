from ICollection import VT, Collection, push_back, seek


# $DEF
def counting_sort(collection: Collection[VT]) -> Collection[VT]:  # $CXGET
    max_ = seek(collection, 0)
    min_ = max_

    buffer = Collection[VT]()

    while not collection.empty:
        el = collection.pop()  # $CX_VAR: pop$
        if el > max_:
            max_ = el
        if el < min_:
            min_ = el
        buffer.push(el)

    counter = [0] * (max_ - min_ + 1)

    while not buffer.empty:
        el = buffer.pop()
        counter[el - min_] += 1

    for i, count in enumerate(counter):
        if count:
            for _ in range(count):
                push_back(collection, i + min_)

    return collection


# $ENDEF
