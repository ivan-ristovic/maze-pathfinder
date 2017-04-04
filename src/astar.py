import traverser
from collections import deque
import heapq

class AStar(traverser.Traverser):

	# Override
	def traverse(self):
		self.initialize()
		self.path = deque()

		heuristic = self.manhattan_heuristic()
		self.astar_traverse(heuristic)

		return list(self.path), self.steps


	# Determining heuristic: Manhattan distance
	def manhattan_heuristic(self):
		h = {}
		for node in self.maze.V:
			h[node] = node.diff(self.maze.end)
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

		# If the maze is not solved, there is no point in reconstruction of the path
		if self.solved == False:
			return

		# Reconstruction of the path
		# FIXME different path length for Dijkstra and Astar for 400.bmp: weeeiiiird???
		self.path.append(self.maze.end)
		current = self.maze.end
		while self.parent_map[current] is not None:
			self.path_length += current.diff(self.parent_map[current]) + 1
			current = self.parent_map[current]
			self.path.append(current)
