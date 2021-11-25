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
    _nop: int = 0
    
    def is_empty(self) -> bool:
        return self._size == 0
    
    def push_back(self, value: VT):
        node = Node[VT](value)
        
        if self.is_empty():
            self._head = node # 1
            self._tail = node # 1
            
            self._nop += 3
            
        else:
            self._tail.next = node # 2
            node.prev = self._tail # 2
            self._tail = node # 1
            
            self._nop += 6
            
        self._size += 1 # 1
    
    def push_front(self, value: VT):
        node = Node[VT](value)
        
        if self.is_empty():
            self._head = node # 1
            self._tail = node # 1
            
            self._nop += 3
            
        else:
            self._head.prev = node # 2
            node.next = self._head # 2
            self._head = node # 1
            
            self._nop += 6

        self._size += 1 # 1
        
    def pop_back(self) -> VT:
        if self.is_empty():
            raise Exception("Can't pop from empty dequeue!")
        
        node = self._tail # 1
        self._tail = node.prev # 2
        self._tail.next = None # 2
        node.prev = None # 2
        self._size -= 1 # 1
        
        self._nop += 8
        
        return node.value
    
    def pop_front(self) -> VT:
        if self.is_empty():
            raise Exception("Can't pop from empty dequeue!")
        
        node = self._head # 1
        self._head = node.next # 2
        self._head.prev = None # 2
        node.next = None # 2
        self._size -= 1 # 1
        
        self._nop += 8
        
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
    def nop(self) -> int:
        return self._nop