from numbers import Real
from typing import List, Optional


class Node:
    left: Optional["Node"]
    right: Optional["Node"]
    value: Real

    def __init__(self, value: Real):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.value)


class BST:
    _root: Optional[Node]

    def __init__(self):
        self._root = None

    def _find(self, root: Node, value: Real):
        if root is None or root.value == value:
            return root

        elif value < root.value:
            return self._find(root.left, value)

        else:
            return self._find(root.right, value)

    def find(self, value):
        return self._find(self._root, value)

    def _insert(self, root: Node, value: Real):
        if root is None:
            return Node(value)

        if value < root.value:
            root.left = self._insert(root.left, value)

        elif value > root.value:
            root.right = self._insert(root.right, value)

        return root

    def insert(self, value: Real):
        self._root = self._insert(self._root, value)

    def _find_min(self, root: Node):
        if root.left is not None:
            return self._find_min(root.left)
        else:
            return root

    def _remove(self, root: Node, value: Real):
        if root is None:
            return None

        if value < root.value:
            root.left = self._remove(root.left, value)
            return root
        elif value > root.value:
            root.right = self._remove(root.right, value)
            return root

        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        else:
            min_value = self._find_min(root.right).value
            root.value = min_value
            root.right = self._remove(root.right, min_value)
            return root

    def remove(self, value: Real):
        self._root = self._remove(self._root, value)

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
            self._traverse_inorder(root.left, nodes_list)
            self._traverse_inorder(root.right, nodes_list)
            nodes_list.append(root)

        return nodes_list

    def traverse_postorder(self) -> List[Node]:
        return self._traverse_postorder(self._root, [])

    def _traverse_preorder(self, root: Node, nodes_list: List[Node]):
        if root is not None:
            nodes_list.append(root)
            self._traverse_inorder(root.left, nodes_list)
            self._traverse_inorder(root.right, nodes_list)

        return nodes_list

    def traverse_preorder(self) -> List[Node]:
        return self._traverse_preorder(self._root, [])
