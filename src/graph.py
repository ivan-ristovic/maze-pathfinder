class Node:
	def __init__(self, x, y, value):
		self.x = x
		self.y = y
		self.visited = False
		# self.val = value


class Graph:

	def form_graph(self, mat, h, w, x, y):
		# TODO


	def __init__(self, pixel_matrix, h, w):
		self.V = []
		self.E = []

		# location starting point and recursively searching paths
		for i in range(w):
			if pixel_matrix[0][i] == 1:
				self.V.append(Node(0, i, "S"))
				self.form_graph(pixel_matrix, h, w, 0, i)
				break;


	def show(self):
		print self.V
		print self.E
