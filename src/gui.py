from PIL import Image
from tkColorChooser import askcolor
import Tkinter
import tkMessageBox, tkFileDialog
import os, sys, time
import subprocess

import imgloader, imgwriter
import graph, traverser
import dfs, bfs, dijkstra, astar
import generator
import filepath


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

		# Main group
		self.grp_solver = Tkinter.LabelFrame(self, text = "Maze solver", padx = 5, pady = 5)
		self.grp_solver.grid(column = 0, row = 0, padx = 10, pady = 5, columnspan = 5)

		# Filename label
		lbl_filename = Tkinter.Label(self.grp_solver,
			anchor = "w",
			text = "Input:"
		)
		lbl_filename.grid(
			column = 0, row = 0,
			sticky = "ew",
			padx = 10, pady = 10
		)

		# Entry for filename
		self.ent_filename = Tkinter.Entry(self.grp_solver)
		self.ent_filename.grid(
			column = 1, row = 0,
			sticky = "ew",
			padx = 10, pady = 10
		)
		self.ent_filename.insert(-1, "normal.bmp")
		self.ent_filename.bind("<Return>", self.ent_filename_on_enter)

		# Button to load image from file
		btn_import = Tkinter.Button(self.grp_solver,
			text = "Import",
			command = self.btn_import_on_click
		)
		btn_import.grid(
			column = 2, row = 0,
			padx = 5, pady = 5
		)

		# Browse button
		btn_import = Tkinter.Button(self.grp_solver,
			text = "Browse",
			command = self.open_dialog
		)
		btn_import.grid(
			column = 3, row = 0,
			padx = 5, pady = 5
		)

		# Group for traverse method radio buttons
		grp_method = Tkinter.LabelFrame(self.grp_solver, text = "Traverse method:", padx = 5, pady = 5)
		grp_method.grid(column = 0, row = 1, padx = 10, pady = 5, columnspan = 4)

		# Radio buttons for the traverse method
		self.rbSelectedValue = Tkinter.StringVar()
		rb_DFS = Tkinter.Radiobutton(grp_method,
			text = "DFS",
			variable = self.rbSelectedValue,
			value = "DFS",
			command = self.disable_heuristic
		)
		rb_BFS = Tkinter.Radiobutton(grp_method,
			text  =  "BFS",
			variable = self.rbSelectedValue,
			value = "BFS",
			command = self.disable_heuristic
		)
		rb_Dijkstra = Tkinter.Radiobutton(grp_method,
			text = "Dijkstra",
			variable = self.rbSelectedValue,
			value = "Dijkstra",
			command = self.disable_heuristic
		)
		rb_Astar = Tkinter.Radiobutton(grp_method,
			text = "A*",
			variable = self.rbSelectedValue,
			value = "Astar",
			command = self.activate_heuristic
		)
		rb_DFS.grid(column = 1, row = 1, padx = 5)
		rb_BFS.grid(column = 2, row = 1, padx = 5)
		rb_Dijkstra.grid(column = 3, row = 1, padx = 5)
		rb_Astar.grid(column = 4, row = 1, padx = 5)
		rb_DFS.select()

		# Group for heuristic
		grp_heuristic = Tkinter.LabelFrame(grp_method, text = "Heuristic (for A*):", padx = 5, pady = 5)
		grp_heuristic.grid(column = 1, row = 2, padx = 10, pady = 5, columnspan = 4)
		self.rb_heuristic_value = Tkinter.IntVar()
		self.rb_heur_manhattan = Tkinter.Radiobutton(grp_heuristic,
			text = "Manhattan",
			variable = self.rb_heuristic_value,
			value = 0
		)
		self.rb_heur_euclidean = Tkinter.Radiobutton(grp_heuristic,
			text = "Euclidean",
			variable = self.rb_heuristic_value,
			value = 1
		)
		self.rb_heur_manhattan.grid(column = 0, row = 0, padx = 5)
		self.rb_heur_euclidean.grid(column = 1, row = 0, padx = 5)
		self.disable_heuristic()

		# Button to solve the maze
		btn_solve = Tkinter.Button(self.grp_solver,
			text = "Solve maze!",
			width = 30,
			command = self.btn_solve_on_click
		)
		btn_solve.grid(column = 1, row = 2, columnspan = 2, pady = 5)

		# Color choosers
		self.btn_color_from = Tkinter.Button(self.grp_solver,
			text = "     ",
			command = self.choose_color_from,
			bg = "#00ff00"
		)
		self.btn_color_to = Tkinter.Button(self.grp_solver,
			text = "     ",
			command = self.choose_color_to,
			bg = "#0000ff"
		)
		self.btn_color_from.grid(column = 0, row = 2)
		self.btn_color_to.grid(column = 3, row = 2)

		# Open solution checkbox
		self.show_solution = Tkinter.IntVar()
		cb_show_solution = Tkinter.Checkbutton(self.grp_solver,
			text = "Open solution when finished",
			variable = self.show_solution
		)
		cb_show_solution.grid(
			column = 0, row = 3,
			columnspan = 5,
			padx = 20, pady = 5
		)
		cb_show_solution.select()

		# Expand button
		self.img_expand = Tkinter.PhotoImage(file=filepath.get_filepath("assets", "expand.gif"))
		self.img_shrink = Tkinter.PhotoImage(file=filepath.get_filepath("assets", "shrink.gif"))
		self.btn_expand = Tkinter.Button(self,
			width = 50, height = 1,
			command = self.toggle_expand
		)
		self.btn_expand.grid(
			column = 0, row = 5,
			columnspan = 5,
			padx = 0, pady = 0
		)
		self.btn_expand.config(image=self.img_expand, height = 20, width = 355)


	def activate_heuristic(self):
		self.rb_heur_manhattan.configure(state = "active")
		self.rb_heur_euclidean.configure(state = "active")


	def disable_heuristic(self):
		self.rb_heur_manhattan.configure(state = "disabled")
		self.rb_heur_euclidean.configure(state = "disabled")


	def choose_color_from(self):
		color = askcolor()
		self.btn_color_from.configure(bg = color[1])


	def choose_color_to(self):
		color = askcolor()
		self.btn_color_to.configure(bg = color[1])


	def toggle_expand(self):
		self.expanded = not self.expanded
		if self.expanded:
			self.btn_expand.config(image=self.img_shrink, height = 20, width = 355)
			# Creating all additional widgets:
			# Group
			self.grp_maze_gen = Tkinter.LabelFrame(self, text = "Maze generator", padx = 5, pady = 5)
			self.grp_maze_gen.grid(column = 0, row = 6, padx = 10, pady = 5, columnspan = 6)
			# Size label
			self.lbl_maze_size = Tkinter.Label(self,
				anchor = "w",
				text = "Maze size: ",
				width = 1
			)
			self.lbl_maze_size.grid(
				column = 1, row = 6,
				sticky = "ew",
				padx = 10, pady = 5
			)
			# Size slider
			self.sld_mazegen_size = Tkinter.Scale(self.grp_maze_gen,
				from_ = 10, to = 70,
				width = 40, length = 170,
				orient = Tkinter.HORIZONTAL
			)
			self.sld_mazegen_size.grid(
				column = 2, row = 6,
				columnspan = 6,
				padx = 0, pady = 0
			)
			# Maze generate button
			self.btn_mazegen = Tkinter.Button(self.grp_maze_gen,
				text = "Generate maze!",
				width = 30,
				command = self.generate_maze
			)
			self.btn_mazegen.grid(
				column = 0, row = 7,
				columnspan = 5,
				padx = 50, pady = 10
			)

		else:
			self.btn_expand.config(image=self.img_expand, height = 20, width = 355)
			# Destroying all widgets
			self.grp_maze_gen.destroy()
			self.lbl_maze_size.destroy()
			self.sld_mazegen_size.destroy()
			self.btn_mazegen.destroy()


	def generate_maze(self):
		size = self.sld_mazegen_size.get()
		generation_time = time.time()
		try:
			mg = generator.MazeGenerator(size, size)
			mg.create_maze("generator_" + str(size) + ".bmp")
		except Exception as e:
			tkMessageBox.showerror("Error", "Error message: " + str(e))
		tkMessageBox.showinfo("Info",
			"Maze successfully created!\n\n" +
			"Elapsed time:\t\t%.5lfs" % (time.time() - generation_time)
		)


	def ent_filename_on_enter(self, event):
		self.btn_import_on_click()


	def open_dialog(self):
		self.filename = tkFileDialog.askopenfilename(
			filetypes = ( ("Picture files", "*.bmp"), ("All files", "*.*") )
		)
		if self.filename:
			try:
				parent_dir, curr_dir = os.path.split(os.getcwd())
				os.chdir(os.path.join(parent_dir, "mazes"))
				self.ent_filename.delete(0, Tkinter.END)
				self.ent_filename.insert(0, os.path.relpath(self.filename))
				os.chdir(os.path.join(parent_dir, "src"))
			except Exception as e:
				tkMessageBox.showerror("Error", "Error message: " + str(e))


	def btn_import_on_click(self):
		# Loading image from file
		loading_time_start = time.time()
		try:
			self.filename = self.ent_filename.get()
			self.img = imgloader.ImageLoader(self.filename)
		except:
			tkMessageBox.showerror("Error",
				"File not found!\n" +
				"Make sure that the maze you are loading is in mazes folder!"
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
			graph_traverser = dijkstra.Dijkstra(self.grp, None)
		elif self.rbSelectedValue.get() == "Astar":
			graph_traverser = astar.AStar(self.grp, self.rb_heuristic_value.get())

		# Traversing the graph and getting traverse node path
		traverse_time_start = time.time()
		try:
			path, steps = graph_traverser.traverse()
		except Exception as e:
			tkMessageBox.showerror("Error", "Error message: " + str(e))
			return
		traverse_time_end = time.time()

		imgwrite_time_start = time.time()
		# Creating new image writer so we can write our new image to the file
		iw = imgwriter.ImageWriter(self.img.mode, self.img.pixel_map, (self.img.w, self.img.h))
		# Applying path to image module
		if isinstance(graph_traverser, astar.AStar):
			iw.apply_path(path, graph_traverser.path_length, self.img.pixel_map, (self.img.w, self.img.h),
				self.btn_color_to.cget("bg"), self.btn_color_from.cget("bg")
			)
		else:
			iw.apply_path(path, graph_traverser.path_length, self.img.pixel_map, (self.img.w, self.img.h),
			self.btn_color_from.cget("bg"), self.btn_color_to.cget("bg")
		)

		# Saving an image of the solved maze
		iw.img.putdata(iw.map_to_list(self.img.pixel_map, (self.img.w, self.img.h)))
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
