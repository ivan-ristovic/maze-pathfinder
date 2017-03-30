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
		parents = {node : None}

		while weight_heap:
			min_weight, min_path, min_node, min_parent = heapq.heappop(weight_heap)
			if min_node == self.maze.end:
				parents[min_node] = min_parent
				self.solved = True
				##visited_nodes.append([min_node, min_parent])
				break;
			# This node is already marked so I don't need to check it
			if self.visited[min_node.x * self.maze.w + min_node.y] == True:
				continue
			self.visited[min_node.x * self.maze.w + min_node.y] = True
			parents[min_node] = min_parent
			for n in min_node.neighbors:
				if self.visited[n.x * self.maze.w + n.y] == False:
					# Distance from min_node to its neighbor
					new_path = min_path + min_node.diff(n)
					new_weight = self.get_heuristic(heuristic, min_node) + new_path
					heapq.heappush(weight_heap, (new_weight, new_path, n, min_node))
					self.steps += 1

		# If the maze is not solved, there is no point in reconstruction of the path
		if self.solved == False:
			return

		# Reconstruction of the path
		self.path.append(self.maze.end)
		current = self.maze.end
		while parents[current] is not None:
			self.path_length += current.diff(parents[current])
			current = parents[current]
			self.path.append(current)
