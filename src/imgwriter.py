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
		new_filename = os.path.join(mazes_path, filename)
		self.img.save(new_filename)
		return new_filename


	# Applies the path to the pixel_map
	def apply_path(self, path, pixel_map, map_size):

		self.reset_map(pixel_map, map_size)

		# For every node in path list: color his location and path to next node

		path_len = len(path)

		it = 0
		for i in range(path_len-1):
			cur = path[i]
			nxt = path[i+1]

			if nxt.x != cur.x:	# Horizontal path
				start = min(nxt.x, cur.x)
				end = max(nxt.x, cur.x)
				while start <= end:
					pixel_map[start][cur.y] = 2
					start += 1
					it += 1
			else:	# Vertical path
				start = min(nxt.y, cur.y)
				end = max(nxt.y, cur.y)
				while start <= end:
					pixel_map[cur.x][start] = 2
					start += 1
					it += 1
		it -= 1

		step = 255.0 / it
		r = 2.0
		for i in range(path_len-1):
			cur = path[i]
			nxt = path[i+1]

			if nxt.x != cur.x:	# Horizontal path
				start = min(nxt.x, cur.x)
				end = max(nxt.x, cur.x)
				while start <= end:
					pixel_map[start][cur.y] = r
					start += 1
					r += step
			else:	# Vertical path
				start = min(nxt.y, cur.y)
				end = max(nxt.y, cur.y)
				while start <= end:
					pixel_map[cur.x][start] = r
					start += 1
					r += step

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
					pixel_list.append((int(pixel_map[x][y]), 0, 255 - int(pixel_map[x][y])))

		return pixel_list


	# Resets the pixel map to delete previous path
	def reset_map(self, pixel_map, map_size):
		for x in range(map_size[1]):
			for y in range(map_size[0]):
				if pixel_map[x][y] >= 2:
					pixel_map[x][y] = 1
