VT = type


class Collection:
    def pop():
        ...

    def push():
        ...

    @property
    def size():
        ...


def swap():
    pass


def seek():
    pass


def counting_sort(collection: Collection[VT]) -> Collection[VT]:  # 4n^2 + 38n + 4
    max_ = seek(collection, 0)  # 2
    min_ = max_  # 2
    for _ in range(collection.size):  # n
        el = collection.pop()  # 7
        if el > max_:  # 1
            max_ = el  # 1
        if el < min_:  # 1
            min_ = el  # 1
        collection.push(el)  # 2n + 9
    # ) = 2n^2 + 20n

    buffer = [0] * (max_ - min_ + 1)  # 1
    for _ in range(collection.size):  # n * (
        el = collection.pop()  # 7
        buffer[el - min_] += 1  # 2
    # ) = 9n

    for i in range(len(buffer)):  # n * (
        for _ in range(buffer[i]):  # k * (
            collection.push(i + min_)  # 2n + 9
        # ) = 2n +9
    # ) = 2n^2 + 9n
