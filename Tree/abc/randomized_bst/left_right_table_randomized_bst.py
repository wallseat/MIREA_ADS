import random
from numbers import Real
from typing import List, Optional


class Node:
    size: int
    value: Real

    def __init__(self, key: Real):
        self.value = key
        self.size = 1

    def __repr__(self):
        return str(self.value)


class RandomizedBST:
    _nodes: List[Node]
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

    def _find(self, root: int, value: Real) -> Optional[int]:
        if root is None or self._nodes[root].value == value:
            return root

        elif value < self._nodes[root].value:
            return self._find(self._left[root], value)

        else:
            return self._find(self._right[root], value)

    def find(self, value: Real) -> Optional[Node]:
        index = self._find(self._root, value)
        return self._nodes[index] if index is not None else None

    def _size(self, root: int) -> int:
        return self._nodes[root].size if root is not None else 0

    def _fix_size(self, root: int):
        self._nodes[root].size = 1 + self._size(self._left[root]) + self._size(self._right[root])

    def _rotate_right(self, d: int) -> Optional[int]:
        b = self._left[d]
        self._left[d] = self._right[b]
        self._right[b] = d
        self._fix_size(d)
        self._fix_size(b)
        return b

    def _rotate_left(self, b: int) -> Optional[int]:
        d = self._right[b]
        self._right[b] = self._left[d]
        self._left[d] = b
        self._fix_size(b)
        self._fix_size(d)
        return d

    def _root_insert(self, root: int, value: Real) -> int:
        if root is None:
            self._nodes.append(Node(value))
            self._left.append(None)
            self._right.append(None)
            return len(self._nodes) - 1

        elif value < self._nodes[root].value:
            self._left[root] = self._root_insert(self._left[root], value)
            return self._rotate_right(root)

        elif value > self._nodes[root].value:
            self._right[root] = self._root_insert(self._right[root], value)
            return self._rotate_left(root)

        else:
            return root

    def _insert(self, root: int, value: Real) -> int:
        if root is None:
            self._nodes.append(Node(value))
            self._left.append(None)
            self._right.append(None)
            return len(self._nodes) - 1

        elif random.randint(0, self._size(root) + 1) == 0:
            return self._root_insert(root, value)

        elif value < self._nodes[root].value:
            self._left[root] = self._insert(self._left[root], value)
            self._fix_size(root)
            return root

        elif value > self._nodes[root].value:
            self._right[root] = self._insert(self._right[root], value)
            self._fix_size(root)
            return root

        else:
            return root

    def insert(self, value: Real):
        self._root = self._insert(self._root, value)

    def _join(self, tree_min: int, tree_max: int) -> int:
        if tree_min is None:
            return tree_max

        elif tree_max is None:
            return tree_min

        elif random.randint(0, self._size(tree_min) + self._size(tree_max)) < self._size(tree_min):
            self._right[tree_min] = self._join(self._right[tree_min], tree_max)
            self._fix_size(tree_min)
            return tree_min

        else:
            self._left[tree_max] = self._join(tree_min, self._left[tree_max])
            self._fix_size(tree_max)
            return tree_max

    def _remove(self, root: int, value: Real) -> Optional[int]:
        if root is None:
            return root

        elif value < self._nodes[root].value:
            self._left[root] = self._remove(self._left[root], value)
            self._fix_size(root)
            return root

        elif value > self._nodes[root].value:
            self._right[root] = self._remove(self._right[root], value)
            self._fix_size(root)
            return root

        else:
            return self._join(self._left[root], self._right[root])

    def remove(self, value: Real):
        self._root = self._remove(self._root, value)

    def _height(self, root: int) -> int:
        if root is None:
            return 0
        else:
            return 1 + max(self._height(self._left[root]), self._height(self._right[root]))

    def height(self) -> int:
        return self._height(self._root)

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
