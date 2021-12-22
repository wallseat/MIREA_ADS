from typing import Generic, TypeVar, List

VT = TypeVar("VT")

class Queue(Generic[VT]):
    _queue: List[VT]
    _nop: int
    
    def __init__(self):
        self._queue = []
        self._nop = 0

    def push(self, value: VT): # n + 2
        self._nop += self.count + 2
        
        self._queue = self._queue.copy() 
        self._queue.append(0)
        # Имитация работы со списком как с массивом. 
        # Создание массива на элемент больше и копирование элементов
        self._queue[-1] = value
        
    def pop(self) -> VT: # n + 2
        self._nop += self.count + 2
        
        if self.is_empty():
            raise Exception("Can't pop from empty queue!")
        
        el = self._queue[0]
        self._queue = self._queue[1:] # создание нового списка на элемент меньше
    
        return el
    
    def is_empty(self) -> bool: # 1
        return len(self._queue) == 0
    
    @property
    def count(self) -> int: # 1
        return len(self._queue)
    
    @property
    def tail(self) -> VT:
        return self._queue[-1]
    
    @property
    def head(self) -> VT:
        return self._queue[0]

    @property
    def n_op(self) -> int:
        return self._nop
    
def print_queue(queue: Queue):
    elems = []
    for _ in range(queue.count): 
        el = queue.pop() 
        elems.append(el) 
        queue.push(el)

    print("Queue[" + ", ".join(map(str, elems)) + "]")
    
def rotate(queue: Queue):
    queue.push(queue.pop())
    
def seek(queue: Queue, pos: int): 
    for _ in range(pos):
        rotate(queue) 

    el = queue.pop()
    queue.push(el)
    
    for _ in range(queue.count - pos - 1):
        rotate(queue)
    
    return el

def pop_by_pos(queue: Queue, pos: int):
    for _ in range(pos):
        rotate(queue) 
        
    el = queue.pop()
    
    for _ in range(queue.count - pos):
        rotate(queue) 
        
    return el

def push_by_pos(queue: Queue, el, pos: int): 
    
    if pos >= queue.count:
        queue.push(el)
        return
    
    for _ in range(pos):
        rotate(queue)
    
    queue.push(el) 
    
    for _ in range(queue.count - pos - 1):
        rotate(queue)
    
def swap(queue: Queue, pos1: int, pos2: int):
    temp = pop_by_pos(queue, pos1)
    push_by_pos(queue, pop_by_pos(queue, pos2 - 1), pos1)
    push_by_pos(queue, temp, pos2)
    
def count_sort(queue: Queue[int]):
    max_elem = None
    min_elem = 0
    
    for _ in range(queue.count):
        el = queue.head
        
        if max_elem is None or el > max_elem:
            max_elem = el
        elif el < min_elem:
            min_elem = el
            
        rotate(queue)
    
    bias = abs(min_elem) + 1
    counter = [0] * (max_elem + bias)
    
    while not queue.is_empty():
        counter[bias + queue.head - 1] += 1
        queue.pop()
    
    
    for i in range(len(counter)):
        if counter[i] == 0:
            continue
        
        for _ in range(counter[i]):
            queue.push(i - bias + 1)


if __name__ == '__main__':
    import time
    from random import randint
    
    tests = 10
    step = 5000
    
    for test_num in range(1, tests + 1):
        queue = Queue[int]()
        for _ in range(test_num * step):
            queue.push(randint(-10000, 10000))
        
        start_time = time.time()
        count_sort(queue)
        total_time = time.time() - start_time
        
        print(f"Test: {test_num}")
        print(f"Elems count: {test_num * step}")
        print(f"Total time: {total_time}")
        print(f"N_OP: {queue.n_op}")
        print("-------------")
        
    
    
    