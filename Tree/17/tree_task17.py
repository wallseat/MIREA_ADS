from typing import Optional, Generic, TypeVar, List

from typing import Optional

VT = TypeVar("VT")


class Node(Generic[VT]):
    value: VT

    def __init__(self, value: VT):
        self.value = value

    def __repr__(self):
        return str(self.value)


class BST(Generic[VT]):
    _nodes: List[Node[VT]]
    _left: List[int]
    _right: List[int]
    _root: Optional[int]

    def __init__(self):
        self._nodes = []
        self._left = []
        self._right = []
        self._root = None

    def _find(self, root: int, value: VT) -> int:
        if root is None or self._nodes[root].value == value:
            return root

        elif value < self._nodes[root].value:
            return self._find(self._left[root], value)

        else:
            return self._find(self._right[root], value)

    def find(self, value) -> Optional[Node[VT]]:
        index = self._find(self._root, value)
        return self._nodes[index] if index is not None else None

    def _insert(self, root: int, value: VT) -> int:
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

    def insert(self, value: VT):
        self._root = self._insert(self._root, value)

    def _find_min(self, root: int) -> Node[VT]:
        if self._left[root] is not None:
            return self._find_min(self._left[root])
        else:
            return self._nodes[root]

    def _remove(self, root: int, value: VT) -> int:
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

    tree_a = BST[int]()
    tree_b = BST[int]()

    for _ in range(15):
        v = randint(-99, 100)

        if randint(0, 99) % 10 >= 7:
            tree_b.insert(v)
        else:
            tree_a.insert(v)

    print("Дерево А в прямом порядке: " + str(tree_a.traverse_preorder()))
    print("Дерево B в симметричном порядке: " + str(tree_b.traverse_inorder()))

    for node in tree_b.traverse_postorder():
        tree_a.insert(node.value)

    print(
        "Дерево А в прямом порядке после добавления элементов дерева B в обратном порядке:\n",
        str(tree_a.traverse_preorder()),
    )
