from typing import Generic, TypeVar, Tuple, Optional, List
from enum import Enum

VT = TypeVar("VT")

class Node(Generic[VT]):
    value: VT
    left: 'Node' = None
    right: 'Node' = None
    
    def __init__(self, value: VT):
        self.value = value
        
    def __str__(self):
        return str(self.value)
    
    def __repr__(self) -> str:
        return f"Node<{self.value}>"

class TreeTraversePath(Enum):
    LINE = 1
    REVERSE = 2
    SYMMETRIC = 3

class Tree(Generic[VT]):
    _root: Node[VT] = None
    
    def _min(self, node: Node[VT]) -> Tuple[Node[VT], Optional[Node[VT]]]:
        node_parent = None
        while node.left:
            node_parent = node
            node = node.left
        return node, node_parent
    
    def _max(self, node: Node[VT]) -> Tuple[Node[VT], Optional[Node[VT]]]:
        node_parent = None
        while node.right:
            node_parent = node
            node = node.right
        return node, node_parent
    
    def _find(self, value: VT) -> Tuple[Node[VT], Optional[Node[VT]]]:
        if self.is_empty():
            raise Exception("Can't find in empty tree!")
        
        parent_node = None
        node = self._root
        while True:
            if node.value > value:
                if node.left:
                    parent_node = node
                    node = node.left
                else:
                    raise Exception(f"Value {value} not found in tree!")
                
            elif node.value < value:
                if node.right:
                    parent_node = node
                    node = node.right
                else:
                    raise Exception(f"Value {value} not found in tree!")
            
            else:
                return node, parent_node
    
    def _traverse(self, node: Node[VT], traverse_path: TreeTraversePath = TreeTraversePath.SYMMETRIC) -> List[VT]:
        path = []
        
        def line(_node: Node):
            if not _node:
                return
            
            path.append(_node.value)
            
            if _node.left:
                line(_node.left)
            if _node.right:
                line(_node.right)
            
        def reverse(_node: Node):
            if not _node:
                return
            
            if _node.left:
                reverse(_node.left)
            if _node.right:
                reverse(_node.right) 
            
            path.append(_node.value)
        
        def symmetric(_node: Node):
            if not _node:
                return
            
            if _node.left:
                symmetric(_node.left)
            
            path.append(_node.value)
                
            if _node.right:
                symmetric(_node.right)
        
        if traverse_path == TreeTraversePath.LINE:
            line(node)
        elif traverse_path == TreeTraversePath.REVERSE:
            reverse(node)
        else:
            symmetric(node)
        
        return path
        
    def _is_root(self, node: Node[VT]) -> bool:
        return node == self._root
    
    def append(self, value: VT):
        if self.is_empty():
            self._root = Node[VT](value)
            
        else:
            node = self._root
            while True:
                if node.value > value:
                    if node.left:
                        node = node.left
                    else:
                        node.left = Node[VT](value)
                        break
                    
                else:
                    if node.right:
                        node = node.right
                    else:
                        node.right = Node[VT](value)
                        break
    
    def remove(self, value: VT):
        
        node, parent_node = self._find(value)
        
        if not node.left and not node.right: # нода - лист
            if self._is_root(node):
                self._root = None
            elif parent_node.right == node:
                parent_node.right = None
            else:
                parent_node.left = None
        
        elif not node.left or not node.right: # нода имеет одного потомка
            if self._is_root(node):
                if node.right:
                    self._root = node.right
                else:
                    self._root = node.left
            
            elif parent_node.right == node:
                parent_node.right = node.right if node.right else node.left
            else:
                parent_node.left = node.right if node.right else node.left
        
        else: # Нода имеет два потомка
            if self._is_root(node):
                left_subtree = node.left
                self._root = node.right
                for value in self._traverse(left_subtree):
                    self.append(value)
                
            elif parent_node.right == node:
                min_node, min_node_parent = self._min(node)
                
                if  min_node_parent.left:
                    min_node_parent.left = None
                
                min_node.left = node.left
                min_node.right = node.right
            
                parent_node.right = min_node
            
            else:
                max_node, max_node_parent = self._max(node)
                
                if max_node_parent.right:
                    max_node_parent.right = None
                
                max_node.right = node.right
                max_node.left = node.left
              
                parent_node.left = max_node
                             
    def is_empty(self) -> bool:
        return self._root is None
    
    def to_str(self, order: TreeTraversePath, is_repr=False):
        func = str
        if is_repr:
            func = repr
            
        data_str = ", ".join(map(func, self._traverse(self._root, order)))
        
        if is_repr:
            return "Tree<[" + data_str + "]>"
        else:
            return data_str
    
    def __str__(self):
        return self.to_str(TreeTraversePath.SYMMETRIC)
    
    def __repr__(self):
        return self.to_str(TreeTraversePath.SYMMETRIC, is_repr=True)
    
    @property
    def root(self):
        return self._root
