from typing import Generic, TypeVar, Optional, List

VT = TypeVar("VT")

class Node(Generic[VT]):
    value: VT
    
    left: Optional['Node[VT]']
    right: Optional['Node[VT]']
    height: int
    
    def __init__(self, value: VT): 
        self.value = value
        
        self.left = None
        self.right = None
        self.height = 1
        
    def __repr__(self):
        return str(self.value)

class AVL_BST(Generic[VT]):
    _root: Node[VT]
    
    def __init__(self):
        self._root = None
    
    def empty(self) -> bool:
        return self._root is None

    def _find(self, root: Node[VT], value: VT) -> Optional[Node[VT]]:
        if root is None or root.value == value:
            return root
        
        elif value < root.value:
            return self._find(root.left, value)
        
        else:
            return self._find(root.right, value)
        
    def find(self, value: VT) -> Optional[Node[VT]]:
        return self._find(self._root, value)
    
    def _fix_height(self, root: Node[VT]):
        root.height = 1 + max(self._height(root.left), self._height(root.right))
        
    def _insert(self, root: Node[VT], value: VT) -> Node[VT]:
        if not root:
            return Node(value)
        
        elif value < root.value:
            root.left = self._insert(root.left, value)
            
        elif value > root.value:
            root.right = self._insert(root.right, value)
            
        else:
            return root

        self._fix_height(root)

        balance_factor = self._balance_factor(root)
        if balance_factor > 1:
            if value < root.left.value:
                return self._right_rotate(root)
            else:
                root.left = self._left_rotate(root.left)
                return self._right_rotate(root)

        if balance_factor < -1:
            if value > root.right.value:
                return self._left_rotate(root)
            else:
                root.right = self._right_rotate(root.right)
                return self._left_rotate(root)

        return root

    def _remove(self, root: Node[VT], value: VT) -> Node[VT]:
        if not root:
            return root
        
        elif value < root.value:
            root.left = self._remove(root.left, value)
            
        elif value > root.value:
            root.right = self._remove(root.right, value)
            
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            
            temp = self._min(root.right)
            root.value = temp.value
            root.right = self._remove(root.right, temp.value)
            
        if root is None:
            return root

        self._fix_height(root)

        balance_factor = self._balance_factor(root)

        if balance_factor > 1:
            if self._balance_factor(root.left) >= 0:
                return self._right_rotate(root)
            else:
                root.left = self._left_rotate(root.left)
                return self._right_rotate(root)
            
        if balance_factor < -1:
            if self._balance_factor(root.right) <= 0:
                return self._left_rotate(root)
            else:
                root.right = self._right_rotate(root.right)
                return self._left_rotate(root)
            
        return root

    def _left_rotate(self, z: Node[VT]) -> Optional[Node[VT]]:
        y = z.right
        z.right = y.left
        y.left = z
        
        self._fix_height(z)
        self._fix_height(y)
        
        return y

    def _right_rotate(self, z: Node[VT]) -> Optional[Node[VT]]:
        y = z.left
        z.left = y.right
        y.right = z
         
        self._fix_height(z)
        self._fix_height(y)
        
        return y

    def _height(self, root: Node[VT]) -> int:
        if not root:
            return 0
        
        return root.height

    def _balance_factor(self, root) -> int:
        if not root:
            return 0
        
        return self._height(root.left) - self._height(root.right)

    def _min(self, root: Node[VT]) -> Node[VT]:
        if root is None or root.left is None:
            return root
        
        return self._min(root.left)

    def height(self) -> int:
        return self._height(self._root)
    
    def insert(self, value: VT):
        self._root = self._insert(self._root, value)
    
    def remove(self, value: VT):
        self._root = self._remove(self._root, value)
    
    def _traverse_inorder(self, root: Node[VT], nodes_list: List[Node[VT]]):
        if root is not None:
            self._traverse_inorder(root.left, nodes_list)
            nodes_list.append(root)
            self._traverse_inorder(root.right, nodes_list)
            
        return nodes_list
    
    def traverse_inorder(self) -> List[Node[VT]]:
        return self._traverse_inorder(self._root, [])

    def _traverse_postorder(self, root: Node[VT], nodes_list: List[Node[VT]]):
        if root is not None:
            self._traverse_postorder(root.left, nodes_list)
            self._traverse_postorder(root.right, nodes_list)
            nodes_list.append(root)
            
        return nodes_list

    def traverse_postorder(self) -> List[Node[VT]]:
        return self._traverse_postorder(self._root, [])
    
    def _traverse_preorder(self, root: Node[VT], nodes_list: List[Node[VT]]):
        if root is not None:
            nodes_list.append(root)
            self._traverse_preorder(root.left, nodes_list)
            self._traverse_preorder(root.left, nodes_list)
            
        return nodes_list

    def traverse_preorder(self) -> List[Node[VT]]:
        return self._traverse_preorder(self._root, [])

if __name__ == '__main__':
    from random import randint
    
    tree_a = AVL_BST[int]()
    tree_b = AVL_BST[int]()
    tree_c = AVL_BST[int]()
    
    for _ in range(15):
        v = randint(-99, 100)
        tree_a.insert(v)
        if randint(0, 29) % 3 == 0:
            tree_b.insert(v)
            
    
    print(f"Дерево А в обратном порядке: {tree_a.traverse_postorder()}\nВысота: {tree_a.height()}")
    print(f"Дерево B в симметричном порядке: {tree_b.traverse_inorder()}\nВысота: {tree_b.height()}")
    
    for elem in tree_a.traverse_postorder():
        if not tree_b.find(elem.value):
            tree_c.insert(elem.value)
    
    print(f"Дерево С после исключения из дерева А элементов дерева В:"
          f"\n{tree_c.traverse_inorder()}"
          f"\nВысота: {tree_c.height()}")