from typing import Optional
from random import randint

class Node:
    left: Optional['Node']
    right: Optional['Node']
    size: int
    
    def __init__(self, value):
        self.left = None
        self.right = None
        self.data = value
        self.size = 0
        
    def __str__(self):
        return f"node<l: {self.left.data if self.left else ''} r: {self.right.data if self.right else ''}>" 


class RandomTree:
    
    @staticmethod
    def get_size(node: Node):
        return node.size if node else 0
    
    def fix_size(self, node: Node):
        node.size = self.get_size(node.left) + self.get_size(node.right) + 1
    
    def rotate_left(self, node: Node):
        l_node = node.left
        if not l_node:
            return node
        
        node.left = l_node.right
        l_node.right = node
        l_node.size = node.size
        
        self.fix_size(node)
        
        return l_node
    
    def rotate_right(self, node: Node):
        r_node = node.right
        if not r_node:
            return node
        
        node.right = r_node.left
        node.left = r_node
        r_node.size = node.size
        
        self.fix_size(node)
        
        return r_node
    
    def insert_root(self, root: Node, data):
        if not root:
            return Node(data)
        
        if data < root.data:
            root.left = self.insert_root(root.left, data)
            return self.rotate_right(root)
        else:
            root.right = self.insert_root(root.right, data)
            return self.rotate_left(root)
    
    def insert(self, root: Node, data):
        if not root:
            return Node(data)
        
        if randint(0, 65536) % (root.size + 1) == 0:
            a = self.insert_root(root, data)
            print(a)
            return a

        if data < root.data:
            root.left = self.insert(root.left, data)

        else:
            root.right = self.insert(root.right, data)

        self.fix_size(root)

        print(root)
        return root

    def search(self, root: Node, data):
        if root is None:
            return None
        
        if root.data == data:
            return root

        if root.data < data:
            return self.search(root.right, data)
        else:
            return self.search(root.left, data)

    def remove(self, root: Node, data):
        if root is None:
            return root

        if data == root.data:
            temp = self.join(root.left, root.right)
            del root
            return temp

        elif data < root.data:
            root.left = self.remove(root.left, data)
            
        else:
            root.right = self.remove(root.right, data)

        return root
    
    def join(self, min_tree: Node, max_tree: Node):
        if min_tree is None:
            return max_tree
        
        if max_tree is None:
            return min_tree
        
        if randint(0, 65536) % (min_tree.size + max_tree.size) < min_tree.size:
            min_tree.right = self.join(min_tree.right, max_tree)
            self.fix_size(min_tree)
            return min_tree
        
        else:
            max_tree.left = self.join(min_tree, max_tree.left)
            self.fix_size(max_tree)
            return max_tree

    def traverse_inorder(self, root: Node):
   
        if root is not None:
            self.traverse_inorder(root.left)
            print(root.data)
            self.traverse_inorder(root.right)

    def traverse_preorder(self, root: Node):
        print(root)
        if root:
            print(root.data)
            self.traverse_preorder(root.left)
            self.traverse_preorder(root.right)

    def traverse_postorder(self, root: Node):
 
        if root:
            self.traverse_postorder(root.left)
            self.traverse_postorder(root.right)
            print(root.data)




tree = RandomTree()
root = None
root = tree.insert(root, 5)
root = tree.insert(root, 0)
root = tree.insert(root, -1)
root = tree.insert(root, 1)
root = tree.insert(root, 7)
root = tree.insert(root, 6)
root = tree.insert(root, 5)
root = tree.insert(root, 0)


