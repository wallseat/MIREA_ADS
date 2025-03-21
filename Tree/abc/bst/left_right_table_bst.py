from numbers import Real
from typing import List, Optional


class Node:
    value: Real

    def __init__(self, value: Real):
        self.value = value

    def __repr__(self):
        return str(self.value)


class BST:
    _nodes: List[Node]
    _left: List[int]
    _right: List[int]
    _root: Optional[int]

    def __init__(self):
        self._nodes = []
        self._left = []
        self._right = []
        self._root = None

    def _find(self, root: int, value: Real) -> int:
        if root is None or self._nodes[root].value == value:
            return root

        elif value < self._nodes[root].value:
            return self._find(self._left[root], value)

        else:
            return self._find(self._right[root], value)

    def find(self, value) -> Optional[Node]:
        index = self._find(self._root, value)
        return self._nodes[index] if index is not None else None

    def _insert(self, root: int, value: Real) -> int:
        if root is None:
            self._nodes.append(Node(value))
            self._left.append(None)
            self._right.append(None)
            return len(self._nodes) - 1

        if value < self._nodes[root].value:
            self._left[root] = self._insert(self._left[root], value)

        elif value > self._nodes[root].value:
            self._right[root] = self._insert(self._right[root], value)

        return root

    def insert(self, value: Real):
        self._root = self._insert(self._root, value)

    def _find_min(self, root: int) -> Node:
        if self._left[root] is not None:
            return self._find_min(self._left[root])
        else:
            return self._nodes[root]

    def _remove(self, root: int, value: Real) -> int:
        if root is None:
            return None

        if value < self._nodes[root].value:
            self._left[root] = self._remove(self._left[root], value)
            return root

        elif value > self._nodes[root].value:
            self._right[root] = self._remove(self._right[root], value)
            return root

        if self._left[root] is None:
            return self._right[root]

        elif self._right[root] is None:
            return self._left[root]

        else:
            min_value = self._find_min(self._right[root]).value
            self._nodes[root].value = min_value
            self._right[root] = self._remove(self._right[root], min_value)

            return root

    def remove(self, value: Real):
        self._root = self._remove(self._root, value)

    def _traverse_inorder(self, root: int, nodes_list: List[Node]):
        if root is not None:
            self._traverse_inorder(self._left[root], nodes_list)
            nodes_list.append(self._nodes[root])
            self._traverse_inorder(self._right[root], nodes_list)

        return nodes_list

    def traverse_inorder(self) -> List[Node]:
        return self._traverse_inorder(self._root, [])

    def _traverse_postorder(self, root: int, nodes_list: List[Node]):
        if root is not None:
            self._traverse_postorder(self._left[root], nodes_list)
            self._traverse_postorder(self._right[root], nodes_list)
            nodes_list.append(self._nodes[root])

        return nodes_list

    def traverse_postorder(self) -> List[Node]:
        return self._traverse_postorder(self._root, [])

    def _traverse_preorder(self, root: Node, nodes_list: List[Node]):
        if root is not None:
            nodes_list.append(self._nodes[root])
            self._traverse_preorder(self._left[root], nodes_list)
            self._traverse_preorder(self._right[root], nodes_list)

        return nodes_list

    def traverse_preorder(self) -> List[Node]:
        return self._traverse_preorder(self._root, [])
