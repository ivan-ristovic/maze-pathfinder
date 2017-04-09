import traverser
from collections import deque

class DFS(traverser.Traverser):

	# Override
	def traverse(self):
		self.initialize()

		self.path = deque()
		self.path.append(self.maze.start)


	def return_result(self, path, steps):
		# Calculating path length
		# TODO efficient: calculate it in traverse functions
		# FIXME path_len is calculating wrong? (MAYBE)
		self.form_path(path)

		return list(path), steps


	def form_path(self, path):
		current = self.maze.start
		for node in path:
			self.path_length += node.diff(current) + 1
			current = node
