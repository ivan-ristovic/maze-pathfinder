import astar
from collections import deque

class Dijkstra(astar.AStar):

	# Override
	def traverse(self):
		self.initialize()
		self.path = deque()
		self.astar_traverse(None)
		return list(self.path), self.steps
