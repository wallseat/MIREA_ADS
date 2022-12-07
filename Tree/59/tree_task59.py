from typing import Generic, List, Optional, TypeVar

VT = TypeVar("VT")


class Node(Generic[VT]):
    left_right: List["Node[VT]"]
    value: VT

    def __init__(self, value: VT):
        self.value = value
        self.left_right = [None, None]

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
            return self._find(root.left_right[0], value)

        else:
            return self._find(root.left_right[1], value)

    def find(self, value):
        return self._find(self._root, value)

    def _insert(self, root: Node[VT], value: VT):
        if root is None:
            return Node(value)

        if value < root.value:
            root.left_right[0] = self._insert(root.left_right[0], value)

        elif value > root.value:
            root.left_right[1] = self._insert(root.left_right[1], value)

        return root

    def insert(self, value: VT):
        self._root = self._insert(self._root, value)

    def _find_min(self, root: Node[VT]):
        if root.left_right[0] is not None:
            return self._find_min(root.left_right[0])
        else:
            return root

    def _remove(self, root: Node[VT], value: VT):
        if root is None:
            return None

        if value < root.value:
            root.left_right[0] = self._remove(root.left_right[0], value)
            return root

        elif value > root.value:
            root.left_right[1] = self._remove(root.left_right[1], value)
            return root

        if root.left_right[0] is None:
            return root.left_right[1]

        elif root.left_right[1] is None:
            return root.left_right[0]

        else:
            min_value = self._find_min(root.left_right[1]).value
            root.value = min_value
            root.left_right[1] = self._remove(root.left_right[1], min_value)
            return root

    def remove(self, value: VT):
        self._root = self._remove(self._root, value)

    def _traverse_inorder(self, root: Node[VT], nodes_list: List[Node[VT]]):
        if root is not None:
            self._traverse_inorder(root.left_right[0], nodes_list)
            nodes_list.append(root)
            self._traverse_inorder(root.left_right[1], nodes_list)

        return nodes_list

    def traverse_inorder(self) -> List[Node[VT]]:
        return self._traverse_inorder(self._root, [])

    def _traverse_postorder(self, root: Node[VT], nodes_list: List[Node[VT]]):
        if root is not None:
            self._traverse_inorder(root.left_right[0], nodes_list)
            self._traverse_inorder(root.left_right[1], nodes_list)
            nodes_list.append(root)

        return nodes_list

    def traverse_postorder(self) -> List[Node[VT]]:
        return self._traverse_postorder(self._root, [])

    def _traverse_preorder(self, root: Node[VT], nodes_list: List[Node[VT]]):
        if root is not None:
            nodes_list.append(root)
            self._traverse_inorder(root.left_right[0], nodes_list)
            self._traverse_inorder(root.left_right[1], nodes_list)

        return nodes_list

    def traverse_preorder(self) -> List[Node[VT]]:
        return self._traverse_preorder(self._root, [])


if __name__ == "__main__":
    from random import randint

    tree_a = BST[int]()
    tree_b = BST[int]()

    for _ in range(15):
        v = randint(-99, 99)
        tree_a.insert(v)

        if randint(0, 10) % 3 == 0:
            tree_b.insert(v)

    print("Дерево A в обратном порядке:\n" + str(tree_a.traverse_postorder()))
    print("Дерево B в симметричном порядке:\n" + str(tree_b.traverse_inorder()))

    for node in tree_a.traverse_inorder():
        if not tree_b.find(node.value):
            tree_a.remove(node.value)

    print(
        "Дерево A после удаления элементов отсутствующих в дереве B:\n"
        + str(tree_a.traverse_postorder())
    )
