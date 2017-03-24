import graph
from collections import deque

class DFS:
	def __init__(self, maze):
		self.steps = 0
		self.solved = False
		self.visited = [False] * maze.w * maze.h
		self.maze = maze

	def solve(self):
		self.solved = False
		self.path = deque()
		self.path.append(self.maze.start)

		#self.solve_dfs_recursive(self.maze.start)
		self.solve_dfs_iterative()

		if self.solved:
			print "Solved in: " , self.steps , "steps"
			return self.path
		else:
			return []

		print "steps: " + str(self.steps)
		if self.solved:
			print "Solved!"
		else:
			print "Not solved!"

	def solve_dfs_recursive(self, node):
		if node == self.maze.end:
			self.solved = True
			return
		else:
			self.visited[node.x * self.maze.w + node.y] = True
			for n in node.neighbors:
				if self.visited[n.x * self.maze.w + n.y] == False:
					self.steps = self.steps + 1
					self.path.append(n)
					self.solve_dfs_recursive(n)
					if not self.solved:
						self.path.pop()
					self.solve_dfs_recursive(n)

	def solve_dfs_iterative(self):
		node = self.maze.start
		stack = deque()
		stack.append(node)
		self.visited[node.x * self.maze.w + node.y] = True
		
		while (stack):
			node = stack.pop()
			#print node.x , ", " , node.y
			if node == self.maze.end:
				self.solved = True
				return
			for n in node.neighbors:
				if self.visited[n.x * self.maze.w + n.y] == False:
					self.visited[n.x * self.maze.w + n.y] = True
					stack.append(n)
					self.steps += 1

