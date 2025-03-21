import random
from numbers import Real
from typing import List, Optional


class Node:
    size: int
    value: Real
    left: Optional["Node"]
    right: Optional["Node"]

    def __init__(self, key: Real):
        self.value = key
        self.size = 1

        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.value)


class RandomizedBST:
    _root: Optional[Node]

    def __init__(self):
        self._root = None

    def empty(self) -> bool:
        return self.root is None

    def _find(self, root: Node, value: Real) -> Optional[Node]:
        if root is None or root.value == value:
            return root

        elif value < root.value:
            return self._find(root.left, value)

        elif value > root.value:
            return self._find(root.right, value)

    def find(self, value: Real) -> Optional[Node]:
        return self._find(self._root, value)

    def _size(self, root: Node) -> int:
        return root.size if root is not None else 0

    def _fix_size(self, root):
        root.size = 1 + self._size(root.left) + self._size(root.right)

    def _rotate_right(self, d: Node) -> Optional[Node]:
        b = d.left
        d.left = b.right
        b.right = d
        self._fix_size(d)
        self._fix_size(b)
        return b

    def _rotate_left(self, b: Node) -> Optional[Node]:
        d = b.right
        b.right = d.left
        d.left = b
        self._fix_size(b)
        self._fix_size(d)
        return d

    def _root_insert(self, root: Node, value: Real) -> Node:
        if root is None:
            return Node(value)

        elif value < root.value:
            root.left = self._root_insert(root.left, value)
            return self._rotate_right(root)

        elif value > root.value:
            root.right = self._root_insert(root.right, value)
            return self._rotate_left(root)

        else:
            return root

    def _insert(self, root: Node, value: Real) -> Node:
        if root is None:
            return Node(value)

        elif random.randint(0, self._size(root) + 1) == 0:
            return self._root_insert(root, value)

        elif value < root.value:
            root.left = self._insert(root.left, value)
            self._fix_size(root)
            return root

        elif value > root.value:
            root.right = self._insert(root.right, value)
            self._fix_size(root)
            return root

        else:
            return root

    def insert(self, value: Real):
        self._root = self._insert(self._root, value)

    def _join(self, tree_min: Node, tree_max: Node) -> Node:
        if tree_min is None:
            return tree_max

        elif tree_max is None:
            return tree_min

        elif random.randint(0, self._size(tree_min) + self._size(tree_max)) < self._size(tree_min):
            tree_min.right = self._join(tree_min.right, tree_max)
            self._fix_size(tree_min)
            return tree_min

        else:
            tree_max.left = self._join(tree_min, tree_max.left)
            self._fix_size(tree_max)
            return tree_max

    def _remove(self, root: Node, value: Real) -> Optional[Node]:
        if root is None:
            return root

        elif value < root.value:
            root.left = self._remove(root.left, value)
            self._fix_size(root)
            return root

        elif value > root.value:
            root.right = self._remove(root.right, value)
            self._fix_size(root)
            return root

        else:
            return self._join(root.left, root.right)

    def remove(self, value: Real):
        self._root = self._remove(self._root, value)

    def _height(self, root: Node) -> int:
        if root is None:
            return 0
        else:
            return 1 + max(self._height(root.left), self._height(root.right))

    def height(self):
        return self._height(self._root)

    def _traverse_inorder(self, root: Node, nodes_list: List[Node]):
        if root is not None:
            self._traverse_inorder(root.left, nodes_list)
            nodes_list.append(root)
            self._traverse_inorder(root.right, nodes_list)

        return nodes_list

    def traverse_inorder(self) -> List[Node]:
        return self._traverse_inorder(self._root, [])

    def _traverse_postorder(self, root: Node, nodes_list: List[Node]):
        if root is not None:
            self._traverse_postorder(root.left, nodes_list)
            self._traverse_postorder(root.right, nodes_list)
            nodes_list.append(root)

        return nodes_list

    def traverse_postorder(self) -> List[Node]:
        return self._traverse_postorder(self._root, [])

    def _traverse_preorder(self, root: Node, nodes_list: List[Node]):
        if root is not None:
            nodes_list.append(root)
            self._traverse_preorder(root.left, nodes_list)
            self._traverse_preorder(root.right, nodes_list)

        return nodes_list

    def traverse_preorder(self) -> List[Node]:
        return self._traverse_preorder(self._root, [])
