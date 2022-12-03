from queue import SimpleQueue

N_OP = 0


def print_queue(queue: SimpleQueue):
    elems = []
    for _ in range(queue.qsize()):
        el = queue.get()
        elems.append(el)
        queue.put(el)

    print(", ".join(map(str, elems)))


def rotate(queue: SimpleQueue):  # 2
    global N_OP

    queue.put(queue.get())  # 2

    N_OP += 2


def seek(queue: SimpleQueue, pos: int):  # 2pos + 3 + 2n - 2pos - 2 = 2n + 1
    global N_OP

    for _ in range(pos):  # 2pos
        rotate(queue)  # 2

    el = queue.get()  # 2
    queue.put(el)  # 1

    for _ in range(queue.qsize() - pos - 1):  # 2n - 2pos - 2
        rotate(queue)  # 2

    N_OP += queue.qsize() * 2 + 1

    return el


def pop_by_pos(queue: SimpleQueue, pos: int):  # 2pos + 2 + 2n - 2pos = 2n + 2
    global N_OP

    for _ in range(pos):  # 2pos
        rotate(queue)  # 2

    el = queue.get()  # 2

    for _ in range(queue.qsize() - pos):  # 2n - 2pos
        rotate(queue)  # 2

    N_OP += queue.qsize() * 2 + 2

    return el


def push_by_pos(
    queue: SimpleQueue, el, pos: int
):  # 2 + 2pos + 1 + 2n - 2pos - 2 = 2n + 1
    global N_OP

    if pos >= queue.qsize():  # 2
        queue.put(el)  # 1

        N_OP += 3
        return

    for _ in range(pos):  # 2pos
        rotate(queue)  # 2

    queue.put(el)  # 1

    for _ in range(queue.qsize() - pos - 1):  # 2n - 2pos - 2
        rotate(queue)  # 2

    N_OP += queue.qsize() * 2 + 1


def swap(queue: SimpleQueue, pos1: int, pos2: int):  # 8n + 7
    temp = pop_by_pos(queue, pos1)  # 2n + 3
    push_by_pos(queue, pop_by_pos(queue, pos2 - 1), pos1)  # 2n + 2 + 2n + 1 = 4n + 3
    push_by_pos(queue, temp, pos2)  # 2n + 1


def heapify(
    queue: SimpleQueue, n: int, i: int
):  # 7 + 8n + 10 + 8n + 7 + log(n) = 16n + log(n) + 14
    largest = i  # 1
    l = 2 * i + 1  # 3
    r = 2 * i + 2  # 3

    if l < n and seek(queue, i) < seek(queue, l):  # 4n + 4
        largest = l  # 1

    if r < n and seek(queue, largest) < seek(queue, r):  # 4n + 4
        largest = r  # 1

    if largest != i:  # 1
        swap(queue, i, largest)  # 8n + 7
        heapify(queue, n, largest)  # ~log(n)


def heap_sort(queue: SimpleQueue):  # 32n^2 + nlog(n) + 21n + 1
    n = queue.qsize()  # 1

    for i in range(
        n // 2 - 1, -1, -1
    ):  # (n // 2) * (16n + log(n) + 14) = 8n^2 + nlog(n)/2 + 7n
        heapify(queue, n, i)

    for i in range(
        n - 1, 0, -1
    ):  # n * (8n + 7 + 16n + log(n) + 14) = 24n^2 + nlog(n) + 14n
        swap(queue, 0, i)
        heapify(queue, i, 0)


if __name__ == "__main__":
    import time
    from random import randint

    tests = 10
    step = 200

    for test_num in range(1, tests + 1):
        N_OP = 0
        queue = SimpleQueue[int]()
        for _ in range(test_num * step):
            queue.put(randint(-10000, 10000))

        start_time = time.time()
        heap_sort(queue)
        total_time = time.time() - start_time

        print(f"Test: {test_num}")
        print(f"Elems count: {test_num * step}")
        print(f"Total time: {total_time}")
        print(f"N_OP: {N_OP}")
        print("-------------")
