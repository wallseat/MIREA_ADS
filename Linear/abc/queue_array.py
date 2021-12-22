from typing import Generic, TypeVar, List

VT = TypeVar("VT")

class Queue(Generic[VT]):
    _queue: List[VT]
    _nop: int
    
    def __init__(self):
        self._queue = []
        self._nop = 0

    def push(self, value: VT): # n + 2
        self._nop += self.size + 2
        
        self._queue = self._queue.copy() 
        self._queue.append(0)
        # Имитация работы со списком как с массивом. 
        # Создание массива на элемент больше и копирование элементов
        self._queue[-1] = value
        
    def pop(self) -> VT: # n + 2
        self._nop += self.size + 2
        
        if self.is_empty():
            raise Exception("Can't pop from empty queue!")
        
        el = self._queue[0]
        self._queue = self._queue[1:] # создание нового списка на элемент меньше
    
        return el
    
    def is_empty(self) -> bool: # 1
        return len(self._queue) == 0
    
    @property
    def size(self) -> int: # 1
        return len(self._queue)
    
    @property
    def tail(self) -> VT:
        return self._queue[-1]
    
    @property
    def head(self) -> VT:
        return self._queue[0]

def print_queue(queue: Queue):
    elems = []
    for _ in range(queue.size): 
        el = queue.pop() 
        elems.append(el) 
        queue.push(el)

    print("Queue[" + ", ".join(map(str, elems)) + "]")

def rotate(queue: Queue):
    queue.push(queue.pop())
    
def seek(queue: Queue[VT], pos: int) -> VT: 
    for _ in range(pos):
        rotate(queue) 

    el = queue.pop()
    queue.push(el)
    
    for _ in range(queue.size - pos - 1):
        rotate(queue)
    
    return el

def pop_by_pos(queue: Queue[VT], pos: int) -> VT:
    for _ in range(pos):
        rotate(queue) 
        
    el = queue.pop()
    
    for _ in range(queue.size - pos):
        rotate(queue) 
        
    return el

def push_by_pos(queue: Queue[VT], el: VT, pos: int): 
    
    if pos >= queue.size:
        queue.push(el)
        return
    
    for _ in range(pos):
        rotate(queue)
    
    queue.push(el) 
    
    for _ in range(queue.size - pos - 1):
        rotate(queue)
    
def swap(queue: Queue, pos1: int, pos2: int):
    temp = pop_by_pos(queue, pos1)
    push_by_pos(queue, pop_by_pos(queue, pos2 - 1), pos1)
    push_by_pos(queue, temp, pos2)

def slice_queue(queue: Queue[VT], l: int = 0, r: int = -1) -> Queue[VT]:
    q = Queue[VT]()
    
    if r == -1:
        r = queue.size - 1
    
    for _ in range(l):
        rotate(queue)
    
    for _ in range(r - l - 1):
        q.push(queue.head)
        rotate(queue)
    
    for _ in range(queue.size - r + 1):
        rotate(queue)
    
    return q

if __name__ == "__main__":
    from random import randint
    queue = Queue[int]()
    test_data = [randint(-100, 100) for _ in range(200)]
    
    for el in test_data:
        queue.push(el)
    
    print_queue(queue)
    
    #1
    for i, el in enumerate(test_data):
        assert seek(queue, i) == el

    # 2    
    test_data.insert(2, 20)
    push_by_pos(queue, 20, 2)
    
    for i, el in enumerate(test_data):
        assert seek(queue, i) == el
    
    # 3
    test_data.pop(2)
    pop_by_pos(queue, 2)
    for i, el in enumerate(test_data):
        assert seek(queue, i) == el
    
    # 4
    tmp = test_data[2]
    test_data[2] = test_data[5]
    test_data[5] = tmp
    
    swap(queue, 2, 5)
    for i, el in enumerate(test_data):
        assert seek(queue, i) == el
    
    # 5
    for _ in range(queue.size):
        test_data.append(test_data.pop(0))
        rotate(queue)
        for i, el in enumerate(test_data):
            assert seek(queue, i) == el
    
    # 6
    for _ in test_data:
        queue.pop()
    
    assert queue.size == 0
    assert queue.is_empty() == True
    
    print("All tests passed")