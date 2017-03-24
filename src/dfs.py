import graph

class DFS:
	def __init__(self, maze):
		self.steps = 0
		self.solved = False
		self.visited = [False] * maze.w * maze.h
		self.maze = maze

	def solve(self):
		self.solved = False
		self.path = [self.maze.start]
		self.solve_dfs_recursive(self.maze.start)

		if self.solved:
			print "Solved in: " , self.steps , "steps"
			return self.path
		else:
			return []


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
						self.path = self.path[0:-1]
