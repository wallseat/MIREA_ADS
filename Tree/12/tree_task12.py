from typing import Generic, List, Optional, TypeVar

VT = TypeVar("VT")


class Node(Generic[VT]):
    left: Optional["Node[VT]"]
    right: Optional["Node[VT]"]
    value: VT

    def __init__(self, value: VT):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.value)


class BST(Generic[VT]):
    _root: Optional[Node[VT]]

    def __init__(self):
        self._root = None

    def _find(self, root: Node[VT], value: VT):
        if root is None or root.value == value:
            return root

        elif value < root.value:
            return self._find(root.left, value)

        else:
            return self._find(root.right, value)

    def find(self, value):
        return self._find(self._root, value)

    def _insert(self, root: Node[VT], value: VT):
        if root is None:
            return Node(value)

        if value < root.value:
            root.left = self._insert(root.left, value)

        elif value > root.value:
            root.right = self._insert(root.right, value)

        return root

    def insert(self, value: VT):
        self._root = self._insert(self._root, value)

    def _find_min(self, root: Node[VT]):
        if root.left is not None:
            return self._find_min(root.left)
        else:
            return root

    def _remove(self, root: Node[VT], value: VT):
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
            self._traverse_inorder(root.left, nodes_list)
            self._traverse_inorder(root.right, nodes_list)
            nodes_list.append(root)

        return nodes_list

    def traverse_postorder(self) -> List[Node[VT]]:
        return self._traverse_postorder(self._root, [])

    def _traverse_preorder(self, root: Node[VT], nodes_list: List[Node[VT]]):
        if root is not None:
            nodes_list.append(root)
            self._traverse_inorder(root.left, nodes_list)
            self._traverse_inorder(root.right, nodes_list)

        return nodes_list

    def traverse_preorder(self) -> List[Node[VT]]:
        return self._traverse_preorder(self._root, [])


if __name__ == "__main__":
    from random import randint

    tree_a = BST[int]()
    tree_b = BST[int]()

    for _ in range(15):
        value = randint(-99, 99)

        if randint(19, 34) % 3 == 2:
            tree_a.insert(value)
        else:
            tree_b.insert(value)

    print("Дерево А в прямом порядке: " + str(tree_a.traverse_preorder()))
    print("Дерево В в симметричном порядке: " + str(tree_a.traverse_inorder()))

    for node in tree_b.traverse_postorder():
        tree_a.insert(node.value)

    print(
        "Дерево А в прямом порядке после добавления дерева В в обратном порядке:\n"
        + str(tree_a.traverse_preorder())
    )
