class Node:
	def __init__(self, x, y, neighbors):
		self.x = x
		self.y = y
		self.neighbors = []
		self.visited = False
		# self.val = value


class Graph:

	# def form_graph(self, mat, h, w, x, y):
		# TODO


	def __init__(self, pixel_matrix, h, w):
		self.V = []


		# upper buffer is used to determine upper neighbor
		upper_buffer = [None] * w
		# location starting point searching paths
		start_pos = 0;
		for i in range(w):
			if pixel_matrix[0][i] == 1:
				start_node = Node(0, i, [])
				self.V.append(start_node)
				upper_buffer[i] = start_node

				# self.form_graph(pixel_matrix, h, w, 0, i)
				break;

		for i in range(1, h - 1):
			left_neighbor = None
			for j in range(1, w - 1):
				# if field is white
				if pixel_matrix[i][j] == 1:
					# should I be a node?
					# giving a code to every possible node
					# 1,2,4,8 if top/right/down/left pixel is white
					code = pixel_matrix[i-1][j] + 2*pixel_matrix[i][j+1] + 4*pixel_matrix[i+1][j] + 8*pixel_matrix[i][j-1]
					if code != 5 and code != 10:
						# I am a node!
						new_node = Node(i, j, [])
						
						# determing neighbors
						# horizontal
						if left_neighbor is not None:
							new_node.neighbors.append(left_neighbor)
							left_neighbor.neighbors.append(new_node)
						
						# vertical
						if upper_buffer[j] is not None:
							new_node.neighbors.append(upper_buffer[j]);
							upper_buffer[j].neighbors.append(new_node)



						self.V.append(new_node)
						left_neighbor = new_node
						upper_buffer[j] = new_node

				elif pixel_matrix[i][j] == 0:
					# there is a wall so the next node won't have left or upper neighbor
					left_neighbor = None
					upper_buffer[j] = None


		# location of the ending node and its neighbors
		for i in range(w):
			if pixel_matrix[h-1][i] == 1:
				end_node = Node(h - 1, i, [])
				end_node.neighbors.append(upper_buffer[i])
				self.V.append(end_node)
				break;

		# print upper_buffer


	def show(self):
		print "Nodes:"
		for node in self.V:
			print "(" + str(node.x) + ", " + str(node.y) + ")\t\tneighbors: ",
			for neighbor in node.neighbors:
				print "(" + str(neighbor.x) + ", " + str(neighbor.y) + ") ",
			print
		print
