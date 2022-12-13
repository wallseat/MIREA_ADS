from typing import Generic, List, Optional, TypeVar

VT = TypeVar("VT")


class Node(Generic[VT]):
    value: VT

    left_right: List["Node[VT]"]
    height: int

    def __init__(self, value: VT):
        self.value = value

        self.left_right = [None, None]
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
            return self._find(root.left_right[0], value)

        else:
            return self._find(root.left_right[1], value)

    def find(self, value: VT) -> Optional[Node[VT]]:
        return self._find(self._root, value)

    def _fix_height(self, root: Node[VT]):
        root.height = 1 + max(
            self._height(root.left_right[0]), self._height(root.left_right[1])
        )

    def _insert(self, root: Node[VT], value: VT) -> Node[VT]:
        if not root:
            return Node(value)

        elif value < root.value:
            root.left_right[0] = self._insert(root.left_right[0], value)

        elif value > root.value:
            root.left_right[1] = self._insert(root.left_right[1], value)

        else:
            return root

        self._fix_height(root)

        balance_factor = self._balance_factor(root)
        if balance_factor > 1:
            if value < root.left_right[0].value:
                return self._right_rotate(root)
            else:
                root.left_right[0] = self._left_rotate(root.left_right[0])
                return self._right_rotate(root)

        if balance_factor < -1:
            if value > root.left_right[1].value:
                return self._left_rotate(root)
            else:
                root.left_right[1] = self._right_rotate(root.left_right[1])
                return self._left_rotate(root)

        return root

    def _remove(self, root: Node[VT], value: VT) -> Node[VT]:
        if not root:
            return root

        elif value < root.value:
            root.left_right[0] = self._remove(root.left_right[0], value)

        elif value > root.value:
            root.left_right[1] = self._remove(root.left_right[1], value)

        else:
            if root.left_right[0] is None:
                temp = root.left_right[1]
                root = None
                return temp

            elif root.left_right[1] is None:
                temp = root.left_right[0]
                root = None
                return temp

            temp = self._min(root.left_right[1])
            root.value = temp.value
            root.left_right[1] = self._remove(root.left_right[1], temp.value)

        if root is None:
            return root

        self._fix_height(root)

        balance_factor = self._balance_factor(root)

        if balance_factor > 1:
            if self._balance_factor(root.left_right[0]) >= 0:
                return self._right_rotate(root)
            else:
                root.left_right[0] = self._left_rotate(root.left_right[0])
                return self._right_rotate(root)

        if balance_factor < -1:
            if self._balance_factor(root.left_right[1]) <= 0:
                return self._left_rotate(root)
            else:
                root.left_right[1] = self._right_rotate(root.left_right[1])
                return self._left_rotate(root)

        return root

    def _left_rotate(self, z: Node[VT]) -> Optional[Node[VT]]:
        y = z.left_right[1]
        z.left_right[1] = y.left_right[0]
        y.left_right[0] = z

        self._fix_height(z)
        self._fix_height(y)

        return y

    def _right_rotate(self, z: Node[VT]) -> Optional[Node[VT]]:
        y = z.left_right[0]
        z.left_right[0] = y.left_right[1]
        y.left_right[1] = z

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

        return self._height(root.left_right[0]) - self._height(root.left_right[1])

    def _min(self, root: Node[VT]) -> Node[VT]:
        if root is None or root.left_right[0] is None:
            return root

        return self._min(root.left_right[0])

    def height(self) -> int:
        return self._height(self._root)

    def insert(self, value: VT):
        self._root = self._insert(self._root, value)

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
            self._traverse_postorder(root.left_right[0], nodes_list)
            self._traverse_postorder(root.left_right[1], nodes_list)
            nodes_list.append(root)

        return nodes_list

    def traverse_postorder(self) -> List[Node[VT]]:
        return self._traverse_postorder(self._root, [])

    def _traverse_preorder(self, root: Node[VT], nodes_list: List[Node[VT]]):
        if root is not None:
            nodes_list.append(root)
            self._traverse_preorder(root.left_right[0], nodes_list)
            self._traverse_preorder(root.left_right[1], nodes_list)

        return nodes_list

    def traverse_preorder(self) -> List[Node[VT]]:
        return self._traverse_preorder(self._root, [])


if __name__ == "__main__":
    from random import randint

    tree_a = AVL_BST[int]()
    tree_b = AVL_BST[int]()
    tree_c = AVL_BST[int]()

    for _ in range(20):
        v = randint(-99, 99)

        tree_a.insert(v)

        if randint(1, 10) % 3 == 1:
            tree_b.insert(v)

    print("Дерево А в прямом порядке: " + str(tree_a.traverse_preorder()))
    print("Дерево В в симметричном порядке: " + str(tree_b.traverse_inorder()))

    for node in tree_a.traverse_preorder():
        if not tree_b.find(node.value):
            tree_c.insert(node.value)
    print(
        "Дерево С полученное удалением из дерева А всех элементов, которые есть в дереве В: "
        + str(tree_c.traverse_inorder())
    )
