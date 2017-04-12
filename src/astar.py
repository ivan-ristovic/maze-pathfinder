import traverser
from collections import deque
import heapq

class AStar(traverser.Traverser):

	# Constructor
	def __init__(self, graph, heuristic):
		# Calling super constructor
		traverser.Traverser.__init__(self, graph)
		# Setting heuristic
		if heuristic == 0:
			self.heuristic = self.manhattan_heuristic()
		else:
			self.heuristic = self.euclidean_heuristic()


	# Override
	def traverse(self):
		self.initialize()
		self.path = deque()

		self.astar_traverse(self.heuristic)

		# If the maze is not solved, there is no point in reconstruction of the path
		if self.solved == True:
			self.form_path()
			return list(self.path), self.steps
		else:
			return [], self.steps


	# Determining heuristic: Manhattan distance
	def manhattan_heuristic(self):
		h = {}
		for node in self.maze.V:
			h[node] = node.diff(self.maze.end)
		return h


	# Determining heuristic: Euclidean distance
	def euclidean_heuristic(self):
		h = {}
		import math
		for node in self.maze.V:
			h[node] = math.sqrt(
				(node.x - self.maze.end.x)*(node.x - self.maze.end.x) +
				(node.y - self.maze.end.y)*(node.y - self.maze.end.y)
			)
		return h


	def get_heuristic(self, heuristic, node):
		if heuristic != None:
			return heuristic[node]
		else:
			return 0


	def astar_traverse(self, heuristic):
		node = self.maze.start
		# Storing heuristic, weight of the path until the node, the node and its parent
		weight_heap = [(self.get_heuristic(heuristic, node), 0, node, None)]
		self.parent_map = {node : None}
		# Closed list is a map of nodes that are finished processing
		closed_list = {}

		while weight_heap:
			min_weight, min_path, min_node, min_parent = heapq.heappop(weight_heap)
			if min_node == self.maze.end:
				self.parent_map[min_node] = min_parent
				self.solved = True
				break;
			# This node is already in the closed so I don't need to check it
			# There's no need to do the algorithm for this node because the heuristic is admissive
			if min_node in closed_list:
				continue
			closed_list[min_node] = True
			self.parent_map[min_node] = min_parent
			for n in min_node.neighbors:
				if n not in closed_list:
					# Distance from min_node to its neighbor
					new_path = min_path + min_node.diff(n)
					new_weight = self.get_heuristic(heuristic, min_node) + new_path
					heapq.heappush(weight_heap, (new_weight, new_path, n, min_node))
					self.steps += 1


	def form_path(self):
		self.path.append(self.maze.end)
		current = self.maze.end
		while self.parent_map[current] is not None:
			self.path_length += current.diff(self.parent_map[current]) + 1
			current = self.parent_map[current]
			self.path.append(current)
