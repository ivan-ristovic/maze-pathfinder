import traverser
from collections import deque

class BFS(traverser.Traverser):

	# Override
	def traverse(self):
		self.initialize()

		self.bfs_traverse()

		# If the maze is not solved, there is no point in reconstruction of the path
		if self.solved == True:
			self.form_path()
			return self.path, self.steps
		else:
			return [], self.steps


	def bfs_traverse(self):
		node_queue = deque()
		node_queue.append(self.maze.start)
		self.parent_map[self.maze.start] = None

		while node_queue:
			node = node_queue.popleft()

			if node == self.maze.end:
				self.solved = True
				break

			for n in node.neighbors:
				if not n in self.parent_map:
					node_queue.append(n)
					self.parent_map[n] = node
					self.steps += 1


	def form_path(self):
		self.path = deque()
		self.path.append(self.maze.end)
		node = self.maze.end
		while node != self.maze.start:
			self.path_length += node.diff(self.parent_map[node]) + 1
			node = self.parent_map[node]
			self.path.appendleft(node)
