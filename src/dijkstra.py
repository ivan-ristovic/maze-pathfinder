import graph
import traverser
from collections import deque
import heapq

class Dijkstra(traverser.Traverser):

	# Override
	def traverse(self):
		self.initialize()
		self.path = deque()

		self.dijkstra_traverse()

		return list(self.path), self.steps


	def dijkstra_traverse(self):
		node = self.maze.start
		# Storing weight of path, a node and a parent
		weight_heap = [(0, node)]
		parents = {node : None}
		visited_nodes = deque()
		visited_nodes.append(node)
		while weight_heap:
			min_weight, min_node = heapq.heappop(weight_heap)
			if min_node == self.maze.end:
				visited_nodes.append(min_node)
				break;
			# This node is already marked so I don't need to check it
			if self.visited[min_node.x * self.maze.w + min_node.y] == True:
				continue
			self.visited[min_node.x * self.maze.w + min_node.y] = True
			visited_nodes.append(min_node)
			for n in min_node.neighbors:
				if self.visited[n.x * self.maze.w + n.y] == False:
					# Distance from min_node to its neighbor
					new_weight = min_weight + max(abs(min_node.x - n.x), abs(min_node.y - n.y))
					parents[n] = min_node
					heapq.heappush(weight_heap, (new_weight, n))
					self.steps += 1

		print min_weight
		min_node.show()

		# Reconstruction of the path
		current = self.maze.end
		self.path.append(current)
		while visited_nodes:
			node = visited_nodes.pop()
			if node == parents[current]:
				self.path.append(node)
				current = node




