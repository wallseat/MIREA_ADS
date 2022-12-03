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
