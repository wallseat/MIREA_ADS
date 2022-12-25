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
    # $А = A ⋂ B$#
    from random import randint

    tree_a = TREE__[int]()
    tree_b = TREE__[int]()

    for _ in range(20):
        value = randint(-99, 99)

        tree_a.insert(value)
        if randint(0, 10) % 3 == 1:
            tree_b.insert(value)

    # $print_A$
    print("Дерево В в симметричном порядке:\n" + str(tree_b.traverse_inorder()))

    for node in tree_a.traverse_inorder():
        if not tree_b.find(node.value):
            tree_a.remove(node.value)

    print(
        "Дерево А после удаления элементов отсутствующих в дереве В:\n"
        + str(tree_a.traverse_inorder())
    )
