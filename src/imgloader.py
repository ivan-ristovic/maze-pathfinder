import os
from PIL import Image

class ImageLoader:

	# Constructor
	def __init__(self, filename):

		self.pixel_map = []
		self.h = 0
		self.w = 0

		# Opening image file
		parent_dir, curr_dir = os.path.split(os.getcwd())
		mazes_path = os.path.join(parent_dir, "mazes")
		im = Image.open(os.path.join(mazes_path, filename))
		im = im.convert("RGB")
		# Getting values from the image object
		pixel_list = list(im.getdata())
		# Getting image size
		self.w, self.h = im.size
		# Getting image mode
		self.mode = im.mode

		# Creating a one-filled pixel map (1 for white (hall), 0 for non-white (wall))
		self.pixel_map = [[1 for i in range(self.w)] for j in range(self.h)]

		# pixel_list iteration counter
		it = 0

		# Filling out pixel_map
		for i in range(self.h):
			for j in range(self.w):
				if pixel_list[it] < (125, 125, 125):
					self.pixel_map[i][j] = 0
				it += 1


	# Prints the pixel_map
	def show(self):
		for row in self.pixel_map:
			for col in row:
				print col,
			print
