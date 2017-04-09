import dfs

class DFSRecursive(dfs.DFS):

	# Override
	def traverse(self):
		dfs.DFS.traverse(self)

		self.dfs_traverse_recursive(self.maze.start)
		if self.solved:
			return dfs.DFS.return_result(self, self.path, self.steps)
		else:
			return [], 0


	def dfs_traverse_recursive(self, node):

		if node == self.maze.end:
			self.solved = True
			return
		else:
			for n in node.neighbors:
				if n not in self.parent_map:
					self.steps = self.steps + 1
					self.path.append(n)
					self.parent_map[n] = node
					self.dfs_traverse_recursive(n)
					if not self.solved:
						self.path.pop()
					else:
						return
