from PIL import Image

class ImageWriter:

	# Constructor
	def __init__(self, mode, pixel_map, size):
		# Creating new image module with given parameters
		self.img = Image.new(mode, size)

		# Transformint map to list and putting list data in our module
		self.img.putdata(self.map_to_list(pixel_map, size))


	# Saves the module to file with a given name
	def write(self, filename):
		self.img.save(filename)


	# Applies the path to the pixel_map
	def apply_path(self, path, pixel_map, map_size):
		# For every node in path list: color his location and path to next node
		for i in range(1, len(path)):
			prev = path[i-1]
			curr = path[i]
			if curr.x != prev.x:	# Horizontal path
				start = min(curr.x, prev.x)
				end = max(curr.x, prev.x)
				while start != end:
					pixel_map[start][prev.y] = 0	# TODO RGB
					start += 1
			else:	# Vertical path
				start = min(curr.y, prev.y)
				end = max(curr.y, prev.y)
				while start != end:
					pixel_map[prev.x][start] = 0	# TODO RGB
					start += 1

		self.img.putdata(self.map_to_list(pixel_map, map_size))


	# Transforms pixel map to pixel list
	def map_to_list(self, pixel_map, map_size):
		# Since we saved the pixels in a matrix, we now need to transform it back to list
		pixel_list = []
		for x in range(map_size[1]):
			for y in range(map_size[0]):
				if pixel_map[x][y] == 0:
					pixel_list.append(0)
				else:
					pixel_list.append(255)

		return pixel_list
