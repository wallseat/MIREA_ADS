from typing import Generic, TypeVar

VT = TypeVar("VT")

class Node(Generic[VT]):
    value: VT
    next: 'Node' = None
    prev: 'Node' = None
    
    def __init__(self, value: VT):
        self.value = value
        
    def __repr__(self) -> str:
        return str(self.value)

class Dequeue(Generic[VT]):
    _head: Node[VT] = None
    _tail: Node[VT] = None
    _size: int = 0
    _n_op: int = 0
    
    def is_empty(self) -> bool:
        return self._size == 0
    
    def push_back(self, value: VT):
        node = Node[VT](value)
        
        if self.is_empty():
            self._head = node # 1
            self._tail = node # 1
            
            self._n_op += 3
            
        else:
            self._tail.next = node # 2
            node.prev = self._tail # 2
            self._tail = node # 1
            
            self._n_op += 6
            
        self._size += 1 # 1
    
    def push_front(self, value: VT):
        node = Node[VT](value)
        
        if self.is_empty():
            self._head = node # 1
            self._tail = node # 1
            
            self._n_op += 3
            
        else:
            self._head.prev = node # 2
            node.next = self._head # 2
            self._head = node # 1
            
            self._n_op += 6

        self._size += 1 # 1
        
    def pop_back(self) -> VT:
        if self.is_empty():
            raise Exception("Can't pop from empty dequeue!")
        
        node = self._tail # 1
        self._tail = node.prev # 2
        self._tail.next = None # 2
        node.prev = None # 2
        self._size -= 1 # 1
        
        self._n_op += 8
        
        return node.value
    
    def pop_front(self) -> VT:
        if self.is_empty():
            raise Exception("Can't pop from empty dequeue!")
        
        node = self._head # 1
        self._head = node.next # 2
        self._head.prev = None # 2
        node.next = None # 2
        self._size -= 1 # 1
        
        self._n_op += 8
        
        return node.value
                
    def __repr__(self) -> str:
        repr_str = ""
        
        node = self._head
        while node is not None:
            repr_str += str(node)
            if node.next is not None:
                repr_str += ", "
            node = node.next
        
        return "dequeue<[" + repr_str + "]>"
    
    @property
    def size(self) -> int:
        return self._size

    @property
    def head(self) -> VT:
        return self._head.value
    
    @property
    def tail(self) -> VT:
        return self._tail.value
    
    @property
    def n_op(self) -> int:
        return self._n_op



def print_dequeue(dequeue: Dequeue):
    elems = []
    for _ in range(dequeue.size): 
        elems.append(dequeue.head) 
        rotate_left(dequeue)

    print("Dequeue[" + ", ".join(map(str, elems)) + "]")    
    
def rotate_left(dequeue: Dequeue): # 8 + 6 = 14
    dequeue.push_back(dequeue.pop_front()) 

def rotate_right(dequeue: Dequeue): # 8 + 6 = 14
    dequeue.push_front(dequeue.pop_back())

def seek(dequeue: Dequeue[VT], index: int) -> VT: # 14n + 8
    if dequeue.is_empty(): # 1
        raise Exception("Can't seek empty dequeue!")
    
    if index >= dequeue.size: # 2
        raise Exception("Index out of range!")
    
    if index >= dequeue.size // 2: # 3
        for _ in range(dequeue.size - index - 1): # 14 * (n / 2) = 7n
            rotate_right(dequeue)
        node = dequeue.tail # 2
        for _ in range(dequeue.size - index - 1): # 7n
            rotate_left(dequeue)
            
        return node

    else:
        for _ in range(index): # 14 * (n / 2) = 7n
            rotate_left(dequeue)
        node = dequeue.head # 2
        for _ in range(index): # 14 * (n / 2) = 7n
            rotate_right(dequeue)
            
        return node

def swap(dequeue: Dequeue, pos1: int, pos2: int): # Σ(0, left_el_pos)(14) + Σ(0, left_el_pos)(14) + Σ(0, right_el_pos - left_el_pos - 1)(14) + 4 + 3 + 7 + 6 + 6 = 28n + 26
    left_el_pos, right_el_pos = min(pos1, pos2), max(pos1, pos2) # 4
    
    if left_el_pos < 0 or right_el_pos >= dequeue.size: # 3
        raise Exception("Invalid position argument!")
    
    if left_el_pos < dequeue.size // 2: # 3
        for _ in range(left_el_pos): # Σ(0, left_el_pos)(14)
            rotate_left(dequeue) # 14
            
        left_el = dequeue.pop_front() # 7
        
        for _ in range(right_el_pos - left_el_pos - 1): # Σ(0, right_el_pos - left_el_pos - 1)(14)
            rotate_left(dequeue) # 14
        
        right_el = dequeue.pop_front() # 7
        
        dequeue.push_front(left_el) # 6
        
        for _ in range(right_el_pos - left_el_pos - 1): # Σ(0, right_el_pos - left_el_pos - 1)(14)
            rotate_right(dequeue)
        
        dequeue.push_front(right_el) # 6
        
        for _ in range(left_el_pos): # Σ(0, left_el_pos)(14)
            rotate_right(dequeue)
            
    else:
        for _ in range(dequeue.size - right_el_pos - 1):
            rotate_right(dequeue)
            
        left_el = dequeue.pop_back()
        
        for _ in range(right_el_pos - left_el_pos - 1):
            rotate_right(dequeue)
        
        right_el = dequeue.pop_back()
        
        dequeue.push_back(left_el)
        
        for _ in range(right_el_pos - left_el_pos - 1):
            rotate_left(dequeue)
        
        dequeue.push_back(right_el)
        
        for _ in range(dequeue.size - right_el_pos - 1):
            rotate_left(dequeue)

def quick_sort(dequeue: Dequeue):
    
    def _quick_sort(left: int, right: int):
        i = left
        j = right
        
        pivot = seek(dequeue, (i + j) // 2)
        
        while i < j:
            while seek(dequeue, i) < pivot:
                i += 1
            while seek(dequeue, j) > pivot:
                j -= 1
        
            if i <= j:
                if i < j:
                    swap(dequeue, i, j)
                i += 1
                j -= 1
        
        if left < j:
            _quick_sort(left, j)
        if i < right:
            _quick_sort(i, right)
                
    _quick_sort(0, dequeue.size - 1)

if __name__ == "__main__":
    import time
    from random import randint
    
    tests = 10
    step = 200
    
    for test_num in range(1, tests + 1):
        dequeue = Dequeue[int]()
        for _ in range(test_num * step):
            dequeue.push_back(randint(-10000, 10000))
        
        start_time = time.time()
        quick_sort(dequeue)
        total_time = time.time() - start_time
        
        print(f"Test: {test_num}")
        print(f"Elems count: {test_num * step}")
        print(f"Total time: {total_time}")
        print(f"N_OP: {dequeue.n_op}")
        print("-------------")
        