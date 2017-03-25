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
			self.dfs_traverse_recursive(self.maze.start)

		return list(self.path), self.steps


	def dfs_traverse_iterative(self):
		# Setting start node
		node = self.maze.start
		self.visited[node.x * self.maze.w + node.y] = True

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
				if self.visited[n.x * self.maze.w + n.y] == False:
					# Put it on top of the stack and mark it as visited
					has_nonvisited_neighbors = True
					self.visited[n.x * self.maze.w + n.y] = True
					self.path.append(n)
					self.steps += 1
					break
			# If we didn't find any neighbors that aren't visited, then pop
			if has_nonvisited_neighbors == False:
				self.path.pop()

			# TODO HACK maybe add label on top of the while loop and just
			# continue that loop when we find one non-visited node?
			# Then there will be no need for this indicator, something like:
			# ...
			# for all neighbors:
			# 	if self.visited[..] = false
			# 		push it
			# 		mark it
			#		continue while
			# path.pop()	- no need for indicator since if we made it here,
			#                 we are sure that it is a dead end


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
