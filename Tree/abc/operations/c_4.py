class TREE__:
    def insert(self):
        ...

    def find(self):
        ...

    def remove(self):
        ...

    def traverse_postorder(self):
        ...

    def traverse_preorder(self):
        ...

    def traverse_inorder(self):
        ...


if __name__ == "__main__":
    # $С = A ⋂ B$#
    from random import randint

    tree_a = TREE__[int]()
    tree_b = TREE__[int]()
    tree_c = TREE__[int]()

    for _ in range(20):
        value = randint(-99, 99)

        tree_a.insert(value)
        if randint(0, 10) % 3 == 1:
            tree_b.insert(value)

    # $print_A$
    print("Дерево В в симметричном порядке:\n" + str(tree_b.traverse_inorder()))

    for node in tree_a.traverse_inorder():
        if tree_b.find(node.value):
            tree_c.insert(node.value)

    print(
        "Дерево C после удаления элементов дерева A отсутствующих в дереве В:\n"
        + str(tree_c.traverse_inorder())
    )
