from typing import Generic, List, Optional, TypeVar

VT = TypeVar("VT")


class Node(Generic[VT]):
    left: Optional["Node[VT]"]
    right: Optional["Node[VT]"]
    parent: Optional["Node[VT]"]
    value: VT

    def __init__(self, value: VT):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

    def __repr__(self):
        return str(self.value)


class BST(Generic[VT]):
    _root: Optional[Node[VT]]

    def __init__(self):
        self._root = None

    def _find(self, root: Node[VT], value: VT) -> Optional[Node[VT]]:
        if root is None or root.value == value:
            return root

        elif value < root.value:
            return self._find(root.left, value)

        else:
            return self._find(root.right, value)

    def find(self, value) -> Optional[Node[VT]]:
        return self._find(self._root, value)

    def _insert(self, root: Node[VT], value: VT) -> Optional[Node[VT]]:
        if root is None:
            return Node(value)

        if value < root.value:
            root.left = self._insert(root.left, value)
            root.left.parent = root

        elif value > root.value:
            root.right = self._insert(root.right, value)
            root.right.parent = root

        return root

    def insert(self, value: VT):
        self._root = self._insert(self._root, value)

    def _find_min(self, root: Node[VT]) -> Node[VT]:
        if root.left is not None:
            return self._find_min(root.left)
        else:
            return root

    def _remove(self, root: Node[VT], value: VT) -> Optional[Node[VT]]:
        if root is None:
            return None

        if value < root.value:
            root.left = self._remove(root.left, value)
            if root.left:
                root.left.parent = root

            return root
        elif value > root.value:
            root.right = self._remove(root.right, value)
            if root.right:
                root.right.parent = root

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

    def _traverse_inorder(self, root: Node[VT], nodes_List: List[Node[VT]]):
        if root is not None:
            self._traverse_inorder(root.left, nodes_List)
            nodes_List.append(root)
            self._traverse_inorder(root.right, nodes_List)

        return nodes_List

    def traverse_inorder(self) -> List[Node[VT]]:
        return self._traverse_inorder(self._root, [])

    def _traverse_postorder(self, root: Node[VT], nodes_List: List[Node[VT]]):
        if root is not None:
            self._traverse_inorder(root.left, nodes_List)
            self._traverse_inorder(root.right, nodes_List)
            nodes_List.append(root)

        return nodes_List

    def traverse_postorder(self) -> List[Node[VT]]:
        return self._traverse_postorder(self._root, [])

    def _traverse_preorder(self, root: Node[VT], nodes_List: List[Node[VT]]):
        if root is not None:
            nodes_List.append(root)
            self._traverse_inorder(root.left, nodes_List)
            self._traverse_inorder(root.right, nodes_List)

        return nodes_List

    def traverse_preorder(self) -> List[Node[VT]]:
        return self._traverse_preorder(self._root, [])


if __name__ == "__main__":

    from random import randint

    tree_a = BST[int]()
    tree_b = BST[int]()

    for _ in range(20):
        value = randint(-99, 99)

        if randint(0, 10) % 3 == 1:
            tree_a.insert(value)
        else:
            tree_b.insert(value)

    print("Дерево А в обратном порядке:\n" + str(tree_a.traverse_postorder()))
    print("Дерево В в симметричном порядке:\n" + str(tree_b.traverse_inorder()))

    for node in tree_b.traverse_preorder():
        tree_a.insert(node.value)

    print(
        "Дерево А после добавления элементов дерева В в прямом порядке:\n"
        + str(tree_a.traverse_inorder())
    )
