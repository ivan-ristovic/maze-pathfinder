import threading
from PIL import Image
import filepath

class ImageLoader:

	# Constructor
	def __init__(self, filename):

		self.pixel_map = []
		self.h = 0
		self.w = 0

		# Opening image file
		im = Image.open(filepath.get_filepath("mazes", filename))
		im = im.convert("RGB")
		# Getting values from the image object
		pixel_list = list(im.getdata())
		# Getting image size
		self.w, self.h = im.size
		# Getting image mode
		self.mode = im.mode

		# Creating a one-filled pixel map (1 for white (hall), 0 for non-white (wall))
		self.pixel_map = [[1 for i in range(self.w)] for j in range(self.h)]

		# Using threads to convert pixel_list into the pixel_map
		# print "Creating threads..."
		t1 = threading.Thread(target = self.fill_out_pixel_map, args = (pixel_list, 0, self.h/2, 0,))
		t2 = threading.Thread(target = self.fill_out_pixel_map, args = (pixel_list, self.h/2, self.h, self.h/2*self.w,))

		# print "Starting threads..."
		t1.start()
		t2.start()
		# Waiting for the threads to finish
		# Program will continue to execute when both threads are finished
		t1.join()
		t2.join()
		# print "Threads are finished!"

	# Prints the pixel_map
	def show(self):
		for row in self.pixel_map:
			for col in row:
				print col,
			print

	# Fills the pixel map from h_min row to h_max row
	# Needed for the treads to determine which segments of the map will which thread process
	def fill_out_pixel_map(self, pixel_list, h_min, h_max, it):
		# print "Starting thread with args ", h_min, h_max, it
		for i in range(h_min, h_max):
			for j in range(self.w):
				if pixel_list[it] < (125, 125, 125):
					self.pixel_map[i][j] = 0
				it += 1
