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


def binary_search_sort(queue: SimpleQueue) -> SimpleQueue:
    """
    Sort  queue using binary search algorithm
    """
    global N_OP

    N_OP = 0

    for i in range(1, queue.qsize()):  # (n - 1) * (
        el = seek(queue, i)  # 2n + 1
        left = 0  # 1
        right = i - 1  # 1

        N_OP += 2 + 2 * queue.qsize() + 1

        while left <= right:  # log2(n - 1) * (
            mid = (left + right) // 2  # 3
            mid_el = seek(queue, mid)  # 2n + 1
            N_OP += 3 + 2 * queue.qsize() + 1

            if el < mid_el:  # 1
                right = mid - 1  # 2
            else:  # 1
                left = mid + 1  # 2

            N_OP += 3
        # ) = log2(n - 1) * (2n + 7)  = 2nlog(n-1) + 7log(n-1)

        swap(queue, left, i)  # 8n + 7
        N_OP += 8 * queue.qsize() + 7
    # ) = 2n^2*log(n-1) + 7nlog(n-1) - 2nlog(n-1) - 7log(n-1) + 2n^2 + n - 2n - 1

    return queue


if __name__ == "__main__":
    import time
    from random import randint

    tests = 10
    step = 300

    for test_num in range(1, tests + 1):
        queue = SimpleQueue[int]()
        for _ in range(test_num * step):
            queue.put(randint(-10000, 10000))

        start_time = time.time()
        binary_search_sort(queue)
        total_time = time.time() - start_time

        print(f"Test: {test_num}")
        print(f"Elems count: {test_num * step}")
        print(f"Total time: {total_time}")
        print(f"N_OP: {N_OP}")
        print("-------------")
