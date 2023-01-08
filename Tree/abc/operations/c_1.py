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
    # $С=A ⋃пр B$
    from itertools import chain
    from random import randint

    tree_a = TREE__()
    tree_b = TREE__()
    tree_c = TREE__()

    for _ in range(20):
        value = randint(-99, 99)

        if randint(0, 10) % 3 == 1:
            tree_a.insert(value)
        else:
            tree_b.insert(value)

    # $print_A$
    print("Дерево В в симметричном порядке:\n" + str(tree_b.traverse_inorder()))

    for node in chain(tree_a.traverse_inorder(), tree_b.traverse_preorder()):
        tree_c.insert(node.value)

    print(
        "Дерево C после добавления элементов дерева В в дерево А прямом порядке:\n"
        + str(tree_c.traverse_inorder())
    )
