import os
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
		parent_dir, curr_dir = os.path.split(os.getcwd())
		mazes_path = os.path.join(parent_dir, "mazes")
		new_filename = os.path.join(mazes_path, "out_" + filename)
		self.img.save(new_filename)


	# Applies the path to the pixel_map
	def apply_path(self, path, pixel_map, map_size):
		# For every node in path list: color his location and path to next node
		for i in range(len(path)-1):
			cur = path[i]
			nxt = path[i+1]
			if nxt.x != cur.x:	# Horizontal path
				start = min(nxt.x, cur.x)
				end = max(nxt.x, cur.x)
				while start <= end:
					pixel_map[start][cur.y] = 2
					start += 1
			else:	# Vertical path
				start = min(nxt.y, cur.y)
				end = max(nxt.y, cur.y)
				while start <= end:
					pixel_map[cur.x][start] = 2
					start += 1

		self.img.putdata(self.map_to_list(pixel_map, map_size))


	# Transforms pixel map to pixel list
	def map_to_list(self, pixel_map, map_size):
		# Since we saved the pixels in a matrix, we now need to transform it back to list
		pixel_list = []
		for x in range(map_size[1]):
			for y in range(map_size[0]):
				if pixel_map[x][y] == 0:
					pixel_list.append((0, 0, 0))
				elif pixel_map[x][y] == 1:
					pixel_list.append((255, 255, 255))
				else:
					pixel_list.append((255, 0, 0))

		return pixel_list
