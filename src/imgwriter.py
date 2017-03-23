from PIL import Image

class ImageWriter:

	# Constructor
	def __init__(self, mode, pixel_map, size):
		# Creating new image module with given parameters
		self.img = Image.new(mode, size)

		# Since we saved the pixels in a matrix, we now need to transform it back to list
		pixel_list = []
		for x in range(size[1]):
			for y in range(size[0]):
				if pixel_map[x][y] == 1:
					pixel_list.append(0)
				else:
					pixel_list.append(255)

		# Putting data to our module
		self.img.putdata(pixel_list)


	# Saves the module to file with a given name
	def write(self, filename):
		self.img.save(filename)
