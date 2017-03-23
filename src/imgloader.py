from PIL import Image

class ImageLoader:

	# Constructor
	def __init__(self, filename):

		self.pixel_map = []
		self.h = 0
		self.w = 0

		# Opening image file
		im = Image.open(filename)
		# Getting values from the image object
		color_list = list(im.getdata())
		# Getting image size
		self.w, self.h = im.size

		# Creating a zero-filled pixel map (0 for white (hall), 1 for non-white (wall))
		self.pixel_map = [[0 for i in range(self.w)] for j in range(self.h)]

		# color_list iteration counter
		it = 0

		# Filling out pixel_map
		for i in range(self.h):
			for j in range(self.w):
				# If the color in the color_list has a value different than
				# white, then set the pixel_map value to 1 (meaning black)
				if color_list[it] != 255:
					self.pixel_map[i][j] = 1
				it += 1


	# Prints the pixel_map
	def show(self):
		for row in self.pixel_map:
			for col in row:
				print col,
			print
