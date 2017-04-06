from PIL import Image
import filepath
import threading

class ImageWriter:

	# Constructor
	def __init__(self, mode, pixel_map, size):
		# Creating new image module with given parameters
		self.img = Image.new(mode, size)


	# Saves the module to file with a given name
	def write(self, filename):
		new_filename = filepath.get_filepath("mazes", filename)
		self.img.save(new_filename)
		return new_filename


	# Applies the path to the pixel_map
	def apply_path(self, path, path_length, pixel_map, map_size, color_start, color_end):
		self.reset_map(pixel_map, map_size)
		nodes_in_path = len(path)

		def hex_to_dec(char):
			if char.isalpha():
				return ord(char) - ord('a') + 10
			else:
				return int(char)

		value_r = hex_to_dec(color_start[1]) * 16 + hex_to_dec(color_start[2])
		value_g = hex_to_dec(color_start[3]) * 16 + hex_to_dec(color_start[4])
		value_b = hex_to_dec(color_start[5]) * 16 + hex_to_dec(color_start[6])

		diff_r = value_r - hex_to_dec(color_end[1]) * 16 - hex_to_dec(color_end[2])
		diff_g = value_g - hex_to_dec(color_end[3]) * 16 - hex_to_dec(color_end[4])
		diff_b = value_b - hex_to_dec(color_end[5]) * 16 - hex_to_dec(color_end[6])

		step_r = float(diff_r) / path_length
		step_g = float(diff_g) / path_length
		step_b = float(diff_b) / path_length

		# For every node in path list: color his location and path to next node
		for i in range(nodes_in_path-1):
			cur = path[i]
			nxt = path[i+1]

			if nxt.x != cur.x:	# Horizontal path
				start = min(nxt.x, cur.x)
				end = max(nxt.x, cur.x)
				while start <= end:
					pixel_map[start][cur.y] = (int(value_r), int(value_g), int(value_b))
					start += 1
					value_r -= step_r
					value_g -= step_g
					value_b -= step_b
			else:	# Vertical path
				start = min(nxt.y, cur.y)
				end = max(nxt.y, cur.y)
				while start <= end:
					pixel_map[cur.x][start] = (int(value_r), int(value_g), int(value_b))
					start += 1
					value_r -= step_r
					value_g -= step_g
					value_b -= step_b


	# Transforms pixel map to pixel list
	def map_to_list(self, pixel_map, map_size):
		# Since we saved the pixels in a matrix, we now need to transform it back to list
		# Next two functions have only local usage
		def to_pixel(x):
			if x == 0:
				return 0
			elif x == 1:
				return (255, 255, 255)
			else:
				# x is a tuple (r, g, b)
				return x

		def part_to_pixel_list(result_map, pixel_map, h_min, h_max, index):
			result = []
			# We use map function to execute to_pixel on every list element in sublist
			for x in range(h_min, h_max):
				result += map(to_pixel, pixel_map[x])
			result_map[index] = result

		# result_map is needed to store the return value of the function
		result_map = {}
		t1 = threading.Thread(target = part_to_pixel_list, args = (result_map, pixel_map, 0, map_size[1]/2, 1, ))
		t2 = threading.Thread(target = part_to_pixel_list, args = (result_map, pixel_map, map_size[1]/2, map_size[1], 2, ))

		t1.start()
		t2.start()

		t1.join()
		t2.join()

		pixel_list = []
		pixel_list += result_map[1]
		pixel_list += result_map[2]

		return pixel_list


	# Resets the pixel map to delete previous path
	def reset_map(self, pixel_map, map_size):
		for x in range(map_size[1]):
			for y in range(map_size[0]):
				if pixel_map[x][y] >= 2:
					pixel_map[x][y] = 1
