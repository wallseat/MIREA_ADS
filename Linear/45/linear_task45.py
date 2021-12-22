from typing import Generic, TypeVar, List

VT = TypeVar("VT")

class Queue(Generic[VT]):
    _queue: List[VT]
    _n_op: int
    
    def __init__(self):
        self._queue = []
        self._n_op = 0

    def push(self, value: VT): # n + 2
        self._n_op += self.size + 2
        
        self._queue = self._queue.copy() 
        self._queue.append(0)
        self._queue[-1] = value
        
    def pop(self) -> VT: # n + 2
        self._n_op += self.size + 2
        
        if self.is_empty():
            raise Exception("Can't pop from empty queue!")
        
        el = self._queue[0]
        self._queue = self._queue[1:]
    
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
    
    @property
    def n_op(self) -> int:
        return self._n_op

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
    
    if r < 0:
        r = queue.size - 1
    
    for _ in range(l):
        rotate(queue)
    
    for _ in range(r - l + 1):
        q.push(queue.head)
        rotate(queue)
    
    for _ in range(queue.size - r - 1):
        rotate(queue)
    
    return q

def merge_sort(queue: Queue):
    def _merge(left: Queue, right: Queue) -> Queue:
        result = Queue()
        i, j = 0, 0
        
        while i < left.size and j < right.size:
            left_v = seek(left, i)
            right_v = seek(right, j)
            
            if left_v < right_v:
                result.push(left_v)
                i += 1
            else:
                result.push(right_v)
                j += 1
        
        while i < left.size:
            result.push(seek(left, i))
            i += 1
        
        while j < right.size:
            result.push(seek(right, j))
            j += 1
        
        return result
                
    
    if queue.size < 2:
        return queue

    middle = queue.size // 2
    left = merge_sort(slice_queue(queue, r=middle - 1))
    right = merge_sort(slice_queue(queue, l=middle))
    return _merge(left, right)

if __name__ == "__main__":
    import time
    from random import randint
    
    tests = 10
    step = 200
    
    for test_num in range(1, tests + 1):
        queue = Queue[int]()
        for _ in range(test_num * step):
            queue.push(randint(-10000, 10000))
        
        start_time = time.time()
        merge_sort(queue)
        total_time = time.time() - start_time
        
        print(f"Test: {test_num}")
        print(f"Elems count: {test_num * step}")
        print(f"Total time: {total_time}")
        print(f"N_OP: {queue.n_op}")
        print("-------------")