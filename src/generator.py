from PIL import Image
from random import shuffle, randrange

class MazeGenerator:

	# Constructor
	def __init__(self, w, h):
		self.w = w
		self.h = h


	def create_maze(self, filename):
		w = self.w / 2
		h = self.h / 2

		# Visited list
		vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]

		# Horizontal and vertical components, zip to view maze
		ver = [["10"] * w + ['1'] for _ in range(h)] + [[]]
		hor = [["11"] * w + ['1'] for _ in range(h + 1)]

		# DFS walk function
		def walk(x, y):
			vis[y][x] = 1

			neighbors = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
			shuffle(neighbors)
			for (xx, yy) in neighbors:
				if vis[yy][xx]: continue
				if xx == x: hor[max(y, yy)][x] = "10"
				if yy == y: ver[y][max(x, xx)] = "00"
				walk(xx, yy)

		# Starting walk
		walk(randrange(w), randrange(h))

		# Solution string
		s = ""
		for (a, b) in zip(hor, ver):
			s += ''.join(a + b)

		# String -> List (for PIL) and print to file
		def print_output(filename):
			# String -> List
			pixel_list = []
			for c in s:
				if c == '0':
					pixel_list.append((255, 255, 255))
				else:
					pixel_list.append(0)

			# Creating starting point
			for i in range(1, self.w):
				if pixel_list[i] == 0 and pixel_list[i + self.w] == (255, 255, 255):
					pixel_list[i] = (255, 255, 255)
					break
			# Creating exit point
			for i in range(len(pixel_list) - 2, len(pixel_list) - self.w, -1):
				if pixel_list[i] == 0 and pixel_list[i - self.w] == (255, 255, 255):
					pixel_list[i] = (255, 255, 255)
					break

			# Writing image to file
			img = Image.new("RGB", (self.w + 1, self.h + 1))
			img.putdata(pixel_list)
			img.save(filename)

		# Printing output
		print_output(filename)
