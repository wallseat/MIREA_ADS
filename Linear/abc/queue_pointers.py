from typing import Generic, TypeVar, Optional

VT = TypeVar("VT")

class Node(Generic[VT]):
    _value: VT
    next: Optional['Node[VT]']
    
    def __init__(self, value: VT, next: Optional['Node[VT]'] = None):
        self._value = value
        self.next = next
    
    @property
    def value(self) -> VT:
        return self._value
    
    def __str__(self) -> str:
        return str(self._value)

class Queue(Generic[VT]):
    _head: Optional[Node[VT]]
    _tail: Optional[Node[VT]]
    _size: int
    _nop: int
    
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0
        self._nop = 0
    
    def push(self, value: VT): # 5
        node = Node(value)
        
        if self.is_empty(): # 1
            self._head = node # 1
            self._tail = node # 1
        else:
            self._tail.next = node # 2
            self._tail = node # 1
        
        self._size += 1 # 1
        self._nop += 4
    
    def pop(self) -> VT: # 6
        if self.is_empty(): # 1
            raise Exception("Can't pop from empty queue!")
        
        node = self._head # 1
        self._head = node.next # 2
        
        if self._head is None: # 1
            self._tail = None # 1
        
        self._size -= 1 # 1
        self._nop += 6
        
        return node.value
    
    def is_empty(self) -> bool:
        return self._size == 0
    
    @property
    def head(self) -> VT:
        return self._head.value
    
    @property
    def tail(self) -> VT:
        return self._tail.value
    
    @property
    def size(self) -> int:
        return self._size

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

    el = queue.head
    
    for _ in range(queue.size - pos):
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