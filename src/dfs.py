import traverser
import tkMessageBox
from collections import deque

class DFS(traverser.Traverser):

	# Override
	def traverse(self):
		self.initialize()

		self.path = deque()
		self.path.append(self.maze.start)
		query = tkMessageBox.askquestion("DFS", "Prefer iterative over recursive?")
		if query == "yes":
			self.dfs_traverse_iterative()
		else:
			self.parent_map[self.maze.start] = None
			self.dfs_traverse_recursive(self.maze.start)

		# Calculating path length
		# TODO efficient: calculate it in traverse functions
		# FIXME path_len is calculating wrong? (MAYBE)
		if self.solved:
			self.form_path()

		return list(self.path), self.steps


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


	def form_path(self):
		current = self.maze.start
		for node in self.path:
			# node.show()
			# print node.diff(current)
			self.path_length += node.diff(current) + 1
			current = node
