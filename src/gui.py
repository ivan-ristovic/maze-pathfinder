from PIL import Image, ImageTk
import Tkinter
import tkMessageBox
import sys
import time

import imgloader
import imgwriter
import graph
import traverser
import dfs
import bfs
import dijkstra
import astar


class Application(Tkinter.Tk):

	# Constructor
	def __init__(self, parent):

		# Calling Tk Constructor since our class is derived from Tkinter.Tk
		Tkinter.Tk.__init__(self, parent)
		# Saving a reference to parent
		self.parent = parent
		# Initializing GUI
		self.initialize()

		# Variables for graph and image module
		self.grp = None
		self.img = None

		self.exec_time = 0

		self.bind('<Escape>', sys.exit)


	def initialize(self):

		# Grid which will contain our widgets
		self.grid()
		# Our window will not be resizable by default
		self.resizable(False, False)

		# Main menu
		menu_MainMenu = Tkinter.Menu(self)
		menu_MainMenu.add_command(label = "Help", command = self.show_help)
		menu_MainMenu.add_command(label = "About", command = self.show_about)
		menu_MainMenu.add_command(label = "Exit", command = sys.exit)
		self.config(menu = menu_MainMenu)

		# Filename label
		lbl_filename = Tkinter.Label(self,
			anchor = "w",
			text = "Filename: "
		)
		lbl_filename.grid(
			column = 0, row = 0,
			sticky = "ew",
			padx = 10, pady = 10
		)

		# Entry for filename
		self.ent_filename = Tkinter.Entry(self)
		self.ent_filename.grid(
			column = 1, row = 0,
			sticky = "ew",
			padx = 10, pady = 10
		)
		self.ent_filename.insert(-1, "normal.bmp")
		self.ent_filename.bind("<Return>", self.ent_filename_on_enter)

		# Button to load image from file
		btn_import = Tkinter.Button(self,
			text = "Import maze!",
			command = self.btn_import_on_click
		)
		btn_import.grid(
			column = 2, row = 0,
			padx = 5, pady = 5
		)

		# Group for traverse method radio buttons
		grp_Method = Tkinter.LabelFrame(self, text = "Traverse method:", padx = 5, pady = 5)
		grp_Method.grid(column = 0, row = 1, padx = 10, pady = 5, columnspan = 3)

		# Radio buttons for the traverse method
		self.rbSelectedValue = Tkinter.StringVar()
		rb_DFS = Tkinter.Radiobutton(grp_Method,
			text = "DFS",
			variable = self.rbSelectedValue,
			value = "DFS"
		)
		rb_BFS = Tkinter.Radiobutton(grp_Method,
			text  =  "BFS",
			variable = self.rbSelectedValue,
			value = "BFS"
		)
		rb_Dijkstra = Tkinter.Radiobutton(grp_Method,
			text = "Dijkstra",
			variable = self.rbSelectedValue,
			value = "Dijkstra"
		)
		rb_Astar = Tkinter.Radiobutton(grp_Method,
			text = "A*",
			variable = self.rbSelectedValue,
			value = "Astar"
		)
		rb_DFS.grid(column = 1, row = 1, padx = 5)
		rb_BFS.grid(column = 2, row = 1, padx = 5)
		rb_Dijkstra.grid(column = 3, row = 1, padx = 5)
		rb_Astar.grid(column = 4, row = 1, padx = 5)
		rb_DFS.select()

		# Button to solve the maze
		btn_solve = Tkinter.Button(self,
			text = "Solve maze!",
			width = 30,
			command = self.btn_solve_on_click
		)
		btn_solve.grid(
			column = 0, row = 2,
			columnspan = 5,
			padx = 20, pady = 10
		)


	def ent_filename_on_enter(self, event):
		self.btn_import_on_click()


	def btn_import_on_click(self):
		# Loading image from file
		loading_time_start = time.time()
		try:
			self.img = imgloader.ImageLoader(self.ent_filename.get())
		except:
			tkMessageBox.showerror("Error",
				"File not found!\n" +
				"Make sure that the maze you are loading is in assets folder!"
			)
			self.img = None
			return

		# Creating graph
		try:
			self.grp = graph.Graph(self.img.pixel_map, self.img.h, self.img.w)
		except:
			tkMessageBox.showerror("Error",
				"Invalid image!\n" +
				"Image must have a black border and only one entry and exit point\n" +
				"Also, the exit point must not have a black square above it."
			)
			self.grp = None
			return

		tkMessageBox.showinfo("Info",
			"Maze successfully imported!\n" +
			"Nodes created: " + str(self.grp.nodes_num) + "\n" +
			"Elapsed time: " + str(time.time() - loading_time_start) + "s!"
		)

		self.exec_time = time.time() - loading_time_start


	def btn_solve_on_click(self):
		if self.grp is None or self.img is None:
			tkMessageBox.showerror("Error", "Please load a maze first!")
			return

		# Creating new graph traverser
		if self.rbSelectedValue.get() == "DFS":
			graph_traverser = dfs.DFS(self.grp)
		elif self.rbSelectedValue.get() == "BFS":
			graph_traverser = bfs.BFS(self.grp)
		elif self.rbSelectedValue.get() == "Dijkstra":
			graph_traverser = dijkstra.Dijkstra(self.grp)
		elif self.rbSelectedValue.get() == "Astar":
			graph_traverser = astar.AStar(self.grp)

		# Traversing the graph and getting traverse node path
		traverse_time_start = time.time()
		path, steps = graph_traverser.traverse()
		traverse_time_end = time.time()
		if path == []:
			tkMessageBox.showerror("Error", "Maze not solved!")
			return	

		imgwrite_time_start = time.time()

		# Creating new image writer so we can write our new image to the file
		iw = imgwriter.ImageWriter(self.img.mode, self.img.pixel_map, (self.img.w, self.img.h))
		# Applying path to image module
		iw.apply_path(path, self.img.pixel_map, (self.img.w, self.img.h))

		# Writing our image to output file
		output_path = iw.write("out_" + self.rbSelectedValue.get() + "_" + self.ent_filename.get())
		imgwrite_time_end = time.time()
		tkMessageBox.showinfo("Info",
			"Solved the maze in " + str(steps) + " steps!\n" +
			"Graph loading time:\t" + str(self.exec_time) + "s\n" +
			"Graph traverse time:\t" + str(traverse_time_end - traverse_time_start) + "s\n" +
			"Path length:\t" + str(graph_traverser.path_length) + "\n" +
			"File writing time:\t" + str(imgwrite_time_end - imgwrite_time_start) + "s\n" +
			"Total execution time:\t" + str(self.exec_time + (imgwrite_time_end - traverse_time_start)) + "s"
		)

		# Showing solution in new window
		self.create_preview_window((self.img.w, self.img.h), output_path)


	# Help window
	def show_help(self):
		tkMessageBox.showinfo("Info",
			"This is a simple program that takes maze input in form of " +
			"an image and solves it using the algorithm of your choice.\n" +
			"The program outputs an image with drawn exit path (if the maze is valid).\n" +
			"Rules for a valid maze:" +
			"\n    1. Everything that is not white will be interpreted as a wall." +
			"\n    2. The maze must have one starting point on top, and one exit point in the bottom" +
			"\n       (if there are multiple entry/exit points, only the first will be used)" +
			"\n    3. The maze must be surrounded by walls (i.e. must be \"closed\")" +
			"\n    4. It is advisable for the corridors to be 1px wide, but it is not mandatory" +
			"\n       (the output will be correct for Dijkstra and A*, but not for DFS or BFS)"
		)


	# About window
	def show_about(self):
		tkMessageBox.showinfo("Info",
			"maze-pathfinder (Beta)\n\n" +
			"Made by Milana Kovacevic and Ivan Ristovic\n\n" +
			"More info at: https://ivan-ristovic.github.io/maze-pathfinder/"
		)


	# Preview window
	def create_preview_window(self, size, file_path):
		# If size is greater than 600x600, then we will not show preview
		if size > (600, 600):
			tkMessageBox.showinfo("Info", "Output image too large for preview!")
			return;

		# Create new window
		window = Tkinter.Toplevel(self)
		window.title("Solution: " + file_path)
		window.geometry(str(size[1]) + "x" + str(size[0]))

		# Opening solution image
		img = ImageTk.PhotoImage(Image.open(file_path))

		# Using label widget to show image as it's background
		panel = Tkinter.Label(window, image = img)
		panel.pack(side = "bottom", fill = "both", expand = "yes")

		window.mainloop()
