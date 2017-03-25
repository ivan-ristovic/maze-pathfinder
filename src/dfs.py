import graph
import traverser
from collections import deque

class DFS(traverser.Traverser):

	def traverse(self):
		self.steps = 0
		self.solved = False
		self.visited = [False] * self.maze.w * self.maze.h
		self.path = deque()
		self.path.append(self.maze.start)

		#self.dfs_traverse_recursive(self.maze.start)
		self.dfs_traverse_iterative()

		if self.solved:
			return self.path, self.steps
		else:
			return [], 0


	def dfs_traverse_recursive(self, node):
		if node == self.maze.end:
			self.solved = True
			return
		else:
			self.visited[node.x * self.maze.w + node.y] = True
			for n in node.neighbors:
				if self.visited[n.x * self.maze.w + n.y] == False:
					self.steps = self.steps + 1
					self.path.append(n)
					self.dfs_traverse_recursive(n)
					if not self.solved:
						self.path.pop()
					else:
						return


	def dfs_traverse_iterative(self):
		node = self.maze.start
		stack = deque()
		stack.append((node, [node]))
		self.visited[node.x * self.maze.w + node.y] = True

		while (stack):
			(node, local_path) = stack.pop()
			if node == self.maze.end:
				self.solved = True
				self.path = local_path
				return
			for n in node.neighbors:
				if self.visited[n.x * self.maze.w + n.y] == False:
					self.visited[n.x * self.maze.w + n.y] = True
					stack.append((n, local_path + [n]))
					self.steps += 1
