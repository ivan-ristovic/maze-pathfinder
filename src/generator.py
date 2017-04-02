from PIL import Image
import random

class MazeGenerator:

	# Constructor
	def __init__(self, size):
		self.pixel_map = [[0 for x in range(size)] for y in range(size)]

		for i in range(size):
			self.pixel_map[0][i] = self.pixel_map[size-1][i] = 1
			self.pixel_map[i][0] = self.pixel_map[i][size-1] = 1


		self.result = self.create_random_maze(1, 1, size-1, size-1);
		self.print_map()


	def create_random_maze(self, start_x, start_y, w, h):
		if w <= 3 or h <= 3:
			return

		orientation = self.choose_orientation(w, h)

		# Determining wall starting point (wx), passage point (px) and wall length
		if orientation == 1:	# horizontal
			wx = start_x
			wy = start_y + random.randint(0, h-3)
			px = wx + random.randint(1, w-2)
			py = wy
			wall_len = w
			dx = 1
			dy = 0
		else:	# vertical
			wx = start_x + random.randint(0, w-3)
			wy = start_y
			px = wx
			py = wy + random.randint(1, h-2)
			wall_len = h
			dx = 0
			dy = 1

		print "start:", start_x, start_y , "w:", w, "h:", h
		print "wx:", wx, "wy:", wy, "px:", px, "py:", py, "len:", wall_len

		# Drawing wall
		for i in range(0, wall_len):
			if wx != px or wy != py:
				self.pixel_map[wy][wx] = 1
			wx += dx
			wy += dy

		self.print_map()
		c = raw_input()

		# Determining parameters for the next recursive call
		if orientation == 1:
			new_w = w
			new_h = wy - start_y + 1
		else:
			new_w = wx - start_x + 1
			new_h = h
		self.create_random_maze(start_x, start_y, new_w, new_h)

		if orientation == 1:
			new_start_x = start_x
			new_start_y = wy + 1
			new_w = w
			new_h = start_y + h - wy - 1
		else:
			new_start_x = wx + 1
			new_start_y = start_y
			new_w = start_x + w - wx - 1
			new_h = h
		self.create_random_maze(new_start_x, new_start_y, new_w, new_h)



	# Returns horizontal or vertical, depending on
	def choose_orientation(self, w, h):
		if w < h:	# horizontal
			return 1
		elif w > h:	# vertical
			return 0
		else:
			return random.randint(0, 1)


	def print_map(self):
		for r in self.pixel_map:
			for c in r:
				print c,
			print


mg = MazeGenerator(15)
