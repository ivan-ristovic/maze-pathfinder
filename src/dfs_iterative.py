import dfs

class DFSIterative(dfs.DFS):

	# Override
	def traverse(self):
		dfs.DFS.traverse(self)

		self.dfs_traverse_iterative()
		if self.solved:
			return dfs.DFS.return_result(self, self.path, self.steps)
		else:
			return [], 0


	def dfs_traverse_iterative(self):
		# Setting start node
		node = self.maze.start
		self.parent_map = {node : None}

		while (self.path):
			# Take a look at top of the stack (DEQUE Y U NO IMPLEMENT POP?)
			node = self.path.pop()
			self.path.append(node)
			# If that is the ending node, then we are done
			if node == self.maze.end:
				self.solved = True
				return
			# Now we need to check if that node has visited neighbors
			has_nonvisited_neighbors = False
			for n in node.neighbors:
				# If we find one that isn't visited
				if n not in self.parent_map:
					# Put it on top of the stack and mark it as visited
					has_nonvisited_neighbors = True
					self.parent_map[n] = node
					self.path.append(n)
					self.steps += 1
					break
			# If we didn't find any neighbors that aren't visited, then pop
			if has_nonvisited_neighbors == False:
				self.path.pop()
