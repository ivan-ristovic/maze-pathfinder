from PIL import Image
import Tkinter
import tkMessageBox, tkFileDialog
import os, sys, time
import subprocess

import imgloader, imgwriter
import graph, traverser
import dfs, bfs, dijkstra, astar
import generator


class Application(Tkinter.Tk):

	# Constructor
	def __init__(self, parent):

		# Our form is in shrink form from start
		self.expanded = False

		# Calling Tk Constructor since our class is derived from Tkinter.Tk
		Tkinter.Tk.__init__(self, parent)
		# Saving a reference to parent
		self.parent = parent
		# Initializing GUI widgets
		self.initialize()

		# Variables for graph and image module
		self.grp = None
		self.img = None

		# Execution time
		self.exec_time = 0

		# Esc to close the program
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
			text = "Import",
			command = self.btn_import_on_click
		)
		btn_import.grid(
			column = 2, row = 0,
			padx = 5, pady = 5
		)

		# Browse button
		btn_import = Tkinter.Button(self,
			text = "Browse",
			command = self.open_dialog
		)
		btn_import.grid(
			column = 3, row = 0,
			padx = 5, pady = 5
		)

		# Group for traverse method radio buttons
		grp_Method = Tkinter.LabelFrame(self, text = "Traverse method:", padx = 5, pady = 5)
		grp_Method.grid(column = 0, row = 1, padx = 10, pady = 5, columnspan = 4)

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
			padx = 20, pady = 5
		)

		# Open solution checkbox
		self.show_solution = Tkinter.IntVar()
		cb_show_solution = Tkinter.Checkbutton(self,
			text = "Open solution when finished",
			variable = self.show_solution
		)
		cb_show_solution.grid(
			column = 0, row = 3,
			columnspan = 5,
			padx = 20, pady = 0
		)
		cb_show_solution.select()

		# Expand button
		self.btn_expand = Tkinter.Button(self,
			text = "v",
			width = 50, height = 1,
			command = self.toggle_expand
		)
		self.btn_expand.grid(
			column = 0, row = 5,
			columnspan = 5,
			padx = 0, pady = 0
		)


	def toggle_expand(self):
		self.expanded = not self.expanded
		if self.expanded:
			# Creating all additional widgets
			self.btn_expand.config(text = "^")
			self.btn_mazegen = Tkinter.Button(self,
				text = "Generate maze!",
				width = 30,
				command = self.generate_maze
			)
			self.btn_mazegen.grid(
				column = 0, row = 6,
				columnspan = 5,
				padx = 10, pady = 10

			)
		else:
			# Destroying all widgets
			self.btn_expand.config(text = "v")
			self.btn_mazegen.destroy()


	def generate_maze(self):
		mg = generator.MazeGenerator(50, 50)
		mg.create_maze("output.bmp")


	def ent_filename_on_enter(self, event):
		self.btn_import_on_click()


	def open_dialog(self):
		self.filename = tkFileDialog.askopenfilename(
			filetypes = ( ("Picture files", "*.bmp"), ("All files", "*.*") )
		)
		if self.filename:
			parent_dir, curr_dir = os.path.split(os.getcwd())
			os.chdir(os.path.join(parent_dir, "mazes"))
			self.ent_filename.delete(0, Tkinter.END)
			self.ent_filename.insert(0, os.path.relpath(self.filename))
			os.chdir(os.path.join(parent_dir, "src"))


	def btn_import_on_click(self):
		# Loading image from file
		loading_time_start = time.time()
		try:
			self.filename = self.ent_filename.get()
			self.img = imgloader.ImageLoader(self.filename)
		except:
			tkMessageBox.showerror("Error",
				"File not found!\n" +
				"Make sure that the maze you are loading is in assets folder!"
			)
			self.img = None
			return

		# Creating graph
		graph_time_start = time.time()
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
		graph_time_end = time.time()

		self.exec_time = graph_time_end - loading_time_start

		tkMessageBox.showinfo("Info",
			"Maze successfully imported!\n\n" +
			"File loading time:\t\t%.5lfs\n" % (graph_time_start - loading_time_start) +
			"Graph creation time:\t\t%.5lfs\n" % (graph_time_end - graph_time_start) +
			"Nodes created:\t\t%u\n" % self.grp.nodes_num +
			"Elapsed time:\t\t%.5lfs" % self.exec_time
		)



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
		try:
			path, steps = graph_traverser.traverse()
		except:
			tkMessageBox.showerror("Error", "Unknown error!")
		traverse_time_end = time.time()
		if path == []:
			tkMessageBox.showerror("Error", "Maze not solved!")
			return

		imgwrite_time_start = time.time()

		# Creating new image writer so we can write our new image to the file
		iw = imgwriter.ImageWriter(self.img.mode, self.img.pixel_map, (self.img.w, self.img.h))
		# Applying path to image module
		iw.apply_path(path, graph_traverser.path_length, self.img.pixel_map, (self.img.w, self.img.h))

		# Writing our image to output file
		output_path = iw.write(self.filename[:-4] + "_" + self.rbSelectedValue.get() + "_out" + ".bmp")

		imgwrite_time_end = time.time()

		tkMessageBox.showinfo("Info",
			"Solved the maze in " + str(steps) + " steps!\n" +
			"Path length:\t\t%d\n" % graph_traverser.path_length +
			"Graph loading time:\t\t%.5lfs\n" % self.exec_time +
			"Graph traverse time:\t\t%.5lfs\n" % (traverse_time_end - traverse_time_start) +
			"File writing time:\t\t%.5lfs\n" % (imgwrite_time_end - imgwrite_time_start) +
			"Total execution time:\t\t%.5lfs" % (self.exec_time + (imgwrite_time_end - traverse_time_start))
		)

		if self.show_solution.get() == 1:
			# Showing solution in new window
			if sys.platform.startswith('linux'):
				subprocess.call(["xdg-open", output_path])
			else:
				os.startfile(output_path)


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
