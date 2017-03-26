import graph
import traverser
from collections import deque
import heapq

class AStar(traverser.Traverser):

	# Override
	def traverse(self):
		self.initialize()
		self.path = deque()

		# Determing heuristic: Manhattan distance
		self.heuristic = {}
		for node in self.maze.V:
			self.heuristic[node] = abs(node.x - self.maze.end.x) + abs(node.y - self.maze.end.y)

		self.astar_traverse()

		return list(self.path), self.steps


	def astar_traverse(self):
		node = self.maze.start
		# Storing heuristic, weight of the path until the node, the node and its parent
		weight_heap = [(self.heuristic[node], 0, node, None)]
		visited_nodes = deque()
		visited_nodes.append([node, None])
		while weight_heap:
			min_weight, min_path, min_node, min_parent = heapq.heappop(weight_heap)
			if min_node == self.maze.end:
				visited_nodes.append([min_node, min_parent])
				break;
			# This node is already marked so I don't need to check it
			if self.visited[min_node.x * self.maze.w + min_node.y] == True:
				continue
			self.visited[min_node.x * self.maze.w + min_node.y] = True
			visited_nodes.append([min_node, min_parent])
			for n in min_node.neighbors:
				if self.visited[n.x * self.maze.w + n.y] == False:
					# Distance from min_node to its neighbor
					new_path = min_path + max(abs(min_node.x - n.x), abs(min_node.y - n.y))
					new_weight = self.heuristic[min_node] + new_path
					heapq.heappush(weight_heap, (new_weight, new_path, n, min_node))
					self.steps += 1


		# Reconstruction of the path
		current, parent = visited_nodes.pop()
		self.path.append(current)
		while visited_nodes:
			node, grand_parent = visited_nodes.pop()
			if node == parent:
				self.path.append(node)
				current = node
				parent = grand_parent

