from typing import Generic, TypeVar, Optional, List

VT = TypeVar("VT")

class Node(Generic[VT]):
    value: VT
    
    height: int
    
    def __init__(self, key: VT): 
        self.value = key
        self.height = 1
        
    def __repr__(self):
        return str(self.value)

class AVL_BST(Generic[VT]):
    _nodes: List[Node[VT]]
    _left: List[int]
    _right: List[int]
    _root: int

    def __init__(self):
        self._root = None
        self._nodes = []
        self._left = []
        self._right = []

    def empty(self) -> bool:
        return self._root is None

    def _find(self, root: int, value: VT) -> Optional[int]:
        if root is None or self._nodes[root].value == value:
            return root
        
        elif value < self._nodes[root].value:
            return self._find(self._left[root], value)
        
        else:
            return self._find(self._right[root], value)
        
    def find(self, value: VT) -> Optional[Node[VT]]:
        index = self._find(self._root, value)
        return self._nodes[index] if index is not None else None
    
    def _fix_height(self, root: int):
        self._nodes[root].height = 1 + max(self._height(self._left[root]), self._height(self._right[root]))
        
    def _insert(self, root: int, value: VT) -> int:
        if root is None:
            self._nodes.append(Node(value))
            self._left.append(None)
            self._right.append(None)
            return len(self._nodes) - 1
        
        elif value < self._nodes[root].value:
            self._left[root] = self._insert(self._left[root], value)
            
        elif value > self._nodes[root].value:
            self._right[root] = self._insert(self._right[root], value)
            
        else:
            return root

        self._fix_height(root)

        balance_factor = self._balance_factor(root)
        if balance_factor > 1:
            if value < self._nodes[self._left[root]].value:
                return self._right_rotate(root)
            else:
                self._left[root] = self._left_rotate(self._left[root])
                return self._right_rotate(root)

        if balance_factor < -1:
            if value > self._nodes[self._right[root]].value:
                return self._left_rotate(root)
            else:
                self._right[root] = self._right_rotate(self._right[root])
                return self._left_rotate(root)

        return root

    def _remove(self, root: int, value: VT) -> int:
        if root is None:
            return root
        
        elif value < self._nodes[root].value:
            self._left[root] = self._remove(self._left[root], value)
            
        elif value > self._nodes[root].value:
            self._right[root] = self._remove(self._right[root], value)
            
        else:
            if self._left[root] is None:
                temp = self._right[root]
                root = None
                return temp
            
            elif self._right[root] is None:
                temp = self._left[root]
                root = None
                return temp
            
            temp = self._min(self._right[root])
            self._nodes[root].value = self._nodes[temp].value
            self._right[root] = self._remove(self._right[root], self._nodes[temp].value)
            
        if root is None:
            return root

        self._fix_height(root)

        balance_factor = self._balance_factor(root)

        if balance_factor > 1:
            if self._balance_factor(self._left[root]) >= 0:
                return self._right_rotate(root)
            else:
                self._left[root] = self._left_rotate(self._left[root])
                return self._right_rotate(root)
            
        if balance_factor < -1:
            if self._balance_factor(self._right[root]) <= 0:
                return self._left_rotate(root)
            else:
                self._right[root] = self._right_rotate(self._right[root])
                return self._left_rotate(root)
            
        return root

    def _left_rotate(self, z: int) -> Optional[int]:
        y = self._right[z]
        self._right[z] = self._left[y]
        self._left[y] = z
        
        self._fix_height(z)
        self._fix_height(y)
        
        return y

    def _right_rotate(self, z: int) -> Optional[int]:
        y = self._left[z]
        self._left[z] = self._right[y]
        self._right[y] = z
         
        self._fix_height(z)
        self._fix_height(y)
        
        return y

    def _height(self, root: int) -> int:
        if root is None:
            return 0
        
        return self._nodes[root].height

    def _balance_factor(self, root: int) -> int:
        if root is None:
            return 0
        
        return self._height(self._left[root]) - self._height(self._right[root])

    def _min(self, root: int) -> int:
        if root is None or self._left[root] is None:
            return root
        
        return self._min(self._left[root])

    def height(self) -> int:
        return self._height(self._root)
    
    def insert(self, value: VT):
        self._root = self._insert(self._root, value)
    
    def remove(self, value: VT):
        self._root = self._remove(self._root, value)

    def _traverse_inorder(self, root: int, nodes_list: List[Node[VT]]):
        if root is not None:
            self._traverse_inorder(self._left[root], nodes_list)
            nodes_list.append(self._nodes[root])
            self._traverse_inorder(self._right[root], nodes_list)
            
        return nodes_list
    
    def traverse_inorder(self) -> List[Node[VT]]:
        return self._traverse_inorder(self._root, [])
    
    def _traverse_postorder(self, root: int, nodes_list: List[Node[VT]]):
        if root is not None:
            self._traverse_postorder(self._left[root], nodes_list)
            self._traverse_postorder(self._right[root], nodes_list)
            nodes_list.append(self._nodes[root])
            
        return nodes_list

    def traverse_postorder(self) -> List[Node[VT]]:
        return self._traverse_postorder(self._root, [])
    
    def _traverse_preorder(self, root: Node[VT], nodes_list: List[Node[VT]]):
        if root is not None:
            nodes_list.append(self._nodes[root])
            self._traverse_preorder(self._left[root], nodes_list)
            self._traverse_preorder(self._right[root], nodes_list)
            
        return nodes_list

    def traverse_preorder(self) -> List[Node[VT]]:
        return self._traverse_preorder(self._root, [])

if __name__ == "__main__":
    from random import randint
    
    tree_a = AVL_BST[int]()
    tree_b = AVL_BST[int]()
    tree_c = AVL_BST[int]()
    
    for _ in range(10):
        value = randint(-99, 99)
        tree_a.insert(value)
        
        if randint(1, 33) % 3 == 0:
            tree_b.insert(value)
            
    print(f"Дерево А в обратном порядке: {tree_a.traverse_postorder()}\nВысота: {tree_a.height()}")
    print(f"Дерево B в обратном порядке: {tree_b.traverse_inorder()}\nВысота: {tree_b.height()}")
    
    for elem in tree_a.traverse_postorder():
        if not tree_b.find(elem.value):
            tree_c.insert(elem.value)
    
    print(f"Дерево С созданное из дерева А исключая элементы дерева B: {tree_c.traverse_inorder()}\nВысота: {tree_c.height()}")