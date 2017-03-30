class Node:
	def __init__(self, x, y, neighbors):
		self.x = x
		self.y = y
		self.neighbors = []
		self.visited = False

	def show(self):
		print "(" + str(self.x) + ", " + str(self.y) + ")"
	
	# Difference between the node and the other node in pixels
	def diff(self, other):
		return abs(self.x - other.x) + abs(self.y - other.y)


class Graph:
	def __init__(self, pixel_matrix, h, w):
		self.start = None
		self.end = None
		self.w = w
		self.h = h
		self.V = []
		self.nodes_num = 0

		# Upper buffer is used to determine upper neighbor
		upper_buffer = [None] * w
		# Locating starting point
		start_pos = 0;
		for i in range(w):
			if pixel_matrix[0][i] == 1:
				self.start = Node(0, i, [])
				self.V.append(self.start)
				upper_buffer[i] = self.start
				break;

		for i in range(1, h - 1):
			left_neighbor = None
			for j in range(1, w - 1):
				# If field is white
				if pixel_matrix[i][j] == 1:
					# Should I be a node?
					# Giving a code to every possible node
					# 1,2,4,8 if top/right/down/left pixel is white
					code = pixel_matrix[i-1][j] + 2*pixel_matrix[i][j+1] + 4*pixel_matrix[i+1][j] + 8*pixel_matrix[i][j-1]
					if code != 5 and code != 10:
						# I am a node!
						new_node = Node(i, j, [])
						self.nodes_num += 1

						# Determining horizontal neighbors
						if left_neighbor is not None:
							new_node.neighbors.append(left_neighbor)
							left_neighbor.neighbors.append(new_node)

						# Determining vertical neighbors
						if upper_buffer[j] is not None:
							new_node.neighbors.append(upper_buffer[j]);
							upper_buffer[j].neighbors.append(new_node)

						self.V.append(new_node)
						left_neighbor = new_node
						upper_buffer[j] = new_node

				elif pixel_matrix[i][j] == 0:
					# This is a wall so the next node won't have left or upper neighbor
					left_neighbor = None
					upper_buffer[j] = None


		# Location of the ending node and it's neighbors
		for i in range(w):
			if pixel_matrix[h-1][i] == 1:
				self.end = Node(h-1, i, [])
				self.end.neighbors.append(upper_buffer[i])
				upper_buffer[i].neighbors.append(self.end)
				self.V.append(self.end)
				break;


	def show(self):
		print "Nodes:"
		for node in self.V:
			node.show()
			print "neighbors: ",
			for neighbor in node.neighbors:
				neighbor.show()
			print
		print
