class Traverser:

	# Constructor
	def __init__(self, maze):
		self.maze = maze


	# Sets all traverse parameters to their initial values
	def initialize(self):
		self.path = []
		self.path_length = 0
		self.steps = 0
		self.solved = False
		# Parent map is used for the path reconstruction determining which nodes
		# are already processed
		self.parent_map = {}


	# Must be implemented in derived classes
	def traverse(self):
		raise NotImplementedError
