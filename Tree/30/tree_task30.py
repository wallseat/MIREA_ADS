import random
from typing import Generic, List, Optional, TypeVar

VT = TypeVar("VT")


class Node(Generic[VT]):
    size: int
    value: VT
    left: Optional["Node[VT]"]
    right: Optional["Node[VT]"]

    def __init__(self, key: VT):
        self.value = key
        self.size = 1

        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.value)


class RandomizedBST(Generic[VT]):
    _root: Optional[Node[VT]]

    def __init__(self):
        self._root = None

    def empty(self) -> bool:
        return self.root is None

    def _find(self, root: Node[VT], value: VT) -> Optional[Node[VT]]:
        if root is None or root.value == value:
            return root

        elif value < root.value:
            return self._find(root.left, value)

        elif value > root.value:
            return self._find(root.right, value)

    def find(self, value: VT) -> Optional[Node[VT]]:
        return self._find(self._root, value)

    def _size(self, root: Node[VT]) -> int:
        return root.size if root is not None else 0

    def _fix_size(self, root):
        root.size = 1 + self._size(root.left) + self._size(root.right)

    def _rotate_right(self, d: Node[VT]) -> Optional[Node[VT]]:
        b = d.left
        d.left = b.right
        b.right = d
        self._fix_size(d)
        self._fix_size(b)
        return b

    def _rotate_left(self, b: Node[VT]) -> Optional[Node[VT]]:
        d = b.right
        b.right = d.left
        d.left = b
        self._fix_size(b)
        self._fix_size(d)
        return d

    def _root_insert(self, root: Node[VT], value: VT) -> Node[VT]:
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

    def _insert(self, root: Node[VT], value: VT) -> Node[VT]:
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

    def insert(self, value: VT):
        self._root = self._insert(self._root, value)

    def _join(self, tree_min: Node[VT], tree_max: Node[VT]) -> Node[VT]:
        if tree_min is None:
            return tree_max

        elif tree_max is None:
            return tree_min

        elif random.randint(
            0, self._size(tree_min) + self._size(tree_max)
        ) < self._size(tree_min):
            tree_min.right = self._join(tree_min.right, tree_max)
            self._fix_size(tree_min)
            return tree_min

        else:
            tree_max.left = self._join(tree_min, tree_max.left)
            self._fix_size(tree_max)
            return tree_max

    def _remove(self, root: Node[VT], value: VT) -> Optional[Node[VT]]:
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

    def remove(self, value: VT):
        self._root = self._remove(self._root, value)

    def _height(self, root: Node[VT]) -> int:
        if root is None:
            return 0
        else:
            return 1 + max(self._height(root.left), self._height(root.right))

    def height(self):
        return self._height(self._root)

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
            self._traverse_preorder(root.right, nodes_list)

        return nodes_list

    def traverse_preorder(self) -> List[Node[VT]]:
        return self._traverse_preorder(self._root, [])


if __name__ == "__main__":
    from random import randint

    tree_a = RandomizedBST[int]()
    tree_b = RandomizedBST[int]()

    for _ in range(20):
        value = randint(-99, 99)
        tree_a.insert(value)
        if randint(7, 53) % 6 >= 4:
            tree_b.insert(value)

    print(f"Дерево А в обратном порядке обхода: {tree_a.traverse_postorder()}")
    print(f"Дерево B в симметричном порядке: {tree_b.traverse_inorder()}")

    for node in tree_b.traverse_inorder():
        tree_a.remove(node.value)

    print(
        f"Дерево А после удаления всех элементов дерева В: {tree_a.traverse_postorder()}"
    )
