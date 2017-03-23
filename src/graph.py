class Node:
	def __init__(self, x, y, neighbors):
		self.x = x
		self.y = y
		neighbors = []
		self.visited = False
		# self.val = value


class Graph:

	# def form_graph(self, mat, h, w, x, y):
		# TODO


	def __init__(self, pixel_matrix, h, w):
		self.V = []

		# location starting point searching paths
		for i in range(w):
			if pixel_matrix[0][i] == 0:
				self.V.append(Node(0, i, []))
				# self.form_graph(pixel_matrix, h, w, 0, i)
				break;

		for i in range(1, h - 1):
			for j in range(1, w - 1):
				# if field is white
				if pixel_matrix[i][j] == 0:
					# should I be a node?
					# giving a code to every possible node
					# 1,2,4,8 if top/right/down/left pixel is white
					# 15 - code because 1 represents a black pixel
					code = 15 - (pixel_matrix[i-1][j] + 2*pixel_matrix[i][j+1] + 4*pixel_matrix[i+1][j] + 8*pixel_matrix[i][j-1])
					if code != 5 and code != 10:
						# I am a node!
						# determing neighbors
						newNeighbors = []
						# horizontal
						# TODO
						# vertical
						# TODO

						self.V.append(Node(i, j, newNeighbors))

		# location of the ending node
		for i in range(w):
			if pixel_matrix[h-1][i] == 0:
				self.V.append(Node(h-1, i, []))
				break;


	def show(self):
		print "Nodes:"
		for node in self.V:
			print str(node.x) + " " + str(node.y) + "\t",
		print
