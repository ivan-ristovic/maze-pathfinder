import Tkinter
import tkMessageBox
import sys

import imgloader
import imgwriter
import graph
import traverser
import dfs
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

		# Variables
		self.grp = None
		self.img = None

		self.bind('<Escape>', sys.exit)


	def initialize(self):

		# Grid which will contain our widgets
		self.grid()
		# Our window will not be resizable by default
		self.resizable(False, False)

		# Main menu
		menu_MainMenu = Tkinter.Menu(self)
		menu_MainMenu.add_command(label = "Help", command = sys.exit)	# TODO
		menu_MainMenu.add_command(label = "About", command = sys.exit)	# TODO
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
		self.rbSelectedValue = Tkinter.IntVar()
		rb_DFS = Tkinter.Radiobutton(grp_Method,
			text = "DFS",
			variable = self.rbSelectedValue,
			value = 1
		)
		rb_BFS = Tkinter.Radiobutton(grp_Method,
			text  =  "BFS",
			variable = self.rbSelectedValue,
			value = 2
		)
		rb_Dijkstra = Tkinter.Radiobutton(grp_Method,
			text = "Dijkstra",
			variable = self.rbSelectedValue,
			value = 3
		)
		rb_Astar = Tkinter.Radiobutton(grp_Method,
			text = "A*",
			variable = self.rbSelectedValue,
			value = 4
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
		tkMessageBox.showinfo("Info", "Maze successfully imported!")


	def btn_solve_on_click(self):
		if self.grp is None or self.img is None:
			tkMessageBox.showerror("Error", "Please load a maze first!")
			return

		# Creating new graph traverser
		if self.rbSelectedValue.get() == 1:
			graph_traverser = dfs.DFS(self.grp)
		elif self.rbSelectedValue.get() == 2:
			graph_traverser = bfs.BFS(self.grp)
		elif self.rbSelectedValue.get() == 3:
			graph_traverser = dijkstra.Dijkstra(self.grp)
		elif self.rbSelectedValue.get() == 4:
			graph_traverser = astar.AStar(self.grp)

		# Traversing the graph and getting traverse node path
		path, steps = graph_traverser.traverse()
		if path == []:		# FIXME MILANA
			tkMessageBox.showerror("Error", "Maze not solved!")
			return

		# Creating new image writer so we can write our new image to the file
		iw = imgwriter.ImageWriter(self.img.mode, self.img.pixel_map, (self.img.w, self.img.h))
		# Applying path to image module
		iw.apply_path(path, self.img.pixel_map, (self.img.w, self.img.h))

		# Writing our image to output file
		iw.write(self.ent_filename.get())
		tkMessageBox.showinfo("Info", "Solved the maze in " + str(steps) + " steps!")
