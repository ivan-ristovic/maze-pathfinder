import traverser
from collections import deque

class BFS(traverser.Traverser):

	# Override
	def traverse(self):
		self.initialize()
		self.bfs_traverse()

		return self.path, self.steps


	def bfs_traverse(self):
		parent_map = {}
		node_queue = deque()
		node_queue.append(self.maze.start)
		self.visited[node.x * self.maze.w + node.y] = True

		while node_queue:
			node = node_queue.popleft()

			if node == self.maze.end:
				self.solved = True
				break

			for n in node.neighbors:
				if self.visited[n.x * self.maze.w + n.y] == False:
					node_queue.append(n)
					parent_map[n] = node
					self.steps += 1

		# Path reconstruction
		if self.solved:
			self.path = deque()
			self.path.append(self.maze.end)
			node = self.maze.end
			while node != self.maze.start:
				node = parent_map[node]
				self.path.appendleft(node)
		else:
			self.path = []
