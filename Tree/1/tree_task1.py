import graphviz

class Node:
	def __init__(self, item):
		self.key = item
		self.left = self.right = None
		self.parent = None

class BinaryTree:
	def __init__(self):
		self.root = None
		self.have_root = False
		self.vis_buff = []

	def visualize(self,name):
		dot = graphviz.Digraph(comment='Binary Tree')
		self.vis_buff_filling(self.root)
		
		dot.edges(self.vis_buff)
		dot.render(f'output/{name}.gv', view=True) 
		

	def vis_buff_filling(self,root)-> None:
		if not root is None:
			try:
				self.vis_buff.append([str(root.parent.key),str(root.key)])
			except:pass
			self.vis_buff_filling(root.left)
			self.vis_buff_filling(root.right)

	def direct_traversal(self,root)-> None:
		if not root is None:
			print("(",root.key, ") ", end = "")
			self.direct_traversal(root.left)
			self.direct_traversal(root.right)

	def symmetric_traversal(self,root)-> None:
		if not root is None:
			self.symmetric_traversal(root.left)
			print("(",root.key, ") ", end = "")
			self.symmetric_traversal(root.right)

	def reverse_traversal(self,root)-> None:
		if not root is None:
			self.reverse_traversal(root.left)
			self.reverse_traversal(root.right)
			print("(",root.key, ") ", end = "")


	def direct_tree_insertion(self,root_from)-> None:
		if not root_from is None:
			self.insert(self.root, root_from.key)
			self.direct_tree_insertion(root_from.left)
			self.direct_tree_insertion(root_from.right)

	def symmetric_tree_insertion(self,root_from)-> None:
		if not root_from is None:
			self.symmetric_tree_insertion(root_from.left)
			self.insert(self.root, root_from.key)
			self.symmetric_tree_insertion(root_from.right)

	def reverse_tree_insertion(self,root_from)-> None:
		if not root_from is None:
			self.reverse_tree_insertion(root_from.left)
			self.reverse_tree_insertion(root_from.right)
			self.insert(self.root, root_from.key)
			
			

	def insert(self,node, key):

		if self.have_root == False:
			self.have_root = True
			self.root = self.insert(self.root, key)
			
			
		
		if node is None:
			return Node(key)

		if key < node.key:
			left_son = self.insert(node.left, key)
			node.left = left_son

			left_son.parent = node
		elif key > node.key:
			right_brother = self.insert(node.right, key)
			node.right = right_brother

			right_brother.parent = node

		return node



	
# Дерево А:
#	   70
#	  /	 \
#	50	  90
#  /  \  /  \
# 40  60 80  100

tree_A = BinaryTree()
tree_A.insert(tree_A.root, 70)
tree_A.insert(tree_A.root, 50)
tree_A.insert(tree_A.root, 40)
tree_A.insert(tree_A.root, 60)
tree_A.insert(tree_A.root, 90)
tree_A.insert(tree_A.root, 80)
tree_A.insert(tree_A.root, 100)

# Дерево B:
#	     75
#	   /   \
#	  55    95
#    /  \  /  \
#   45  65 85  105
#  /
# 35

tree_B = BinaryTree()


tree_B.insert(tree_B.root, 75)
tree_B.insert(tree_B.root, 55)
tree_B.insert(tree_B.root, 45)
tree_B.insert(tree_B.root, 65)
tree_B.insert(tree_B.root, 35)
tree_B.insert(tree_B.root, 95)
tree_B.insert(tree_B.root, 85)
tree_B.insert(tree_B.root, 105)


tree_C=BinaryTree()

# Дерево C:
#	            70
#	     /             \
#       50              90
#      /  \            /  \
#     40     60     80     100
#    /  \   /  \   /  \    /  \
#   35  45 55  65 75   85 95  105


print("\nСимметричный обход:")
tree_A.symmetric_traversal(tree_A.root)
print("\nПрямой обход :")
tree_A.direct_traversal(tree_A.root)
print("\nОбратный обход: ")
tree_A.reverse_traversal(tree_A.root)


print("\nДобавление элементов одного дерева в другое в прямом обходе: ")
tree_C.direct_tree_insertion(tree_A.root)
tree_C.direct_tree_insertion(tree_B.root)

tree_C.direct_traversal(tree_C.root)

print("\nВизуализация дерева: ")
tree_A.visualize("A_binary_tree")
tree_B.visualize("B_binary_tree")
tree_C.visualize("C_binary_tree")


