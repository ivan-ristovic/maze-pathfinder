import Tkinter
import tkMessageBox
import sys

import imgloader
import imgwriter
import graph
import dfs


class Application(Tkinter.Tk):

	# Constructor
	def __init__(self, parent):

		# Calling Tk Constructor since our class is derived from Tkinter.Tk
		Tkinter.Tk.__init__(self, parent)
		# Saving a reference to parent
		self.parent = parent
		# Initializing GUI
		self.initialize()

		self.bind('<Escape>', sys.exit)


	def initialize(self):

		# Grid which will contain our widgets
		self.grid()
		# Our window will not be resizable by default
		self.resizable(False, False)

		# Filename label
		lbl_filename = Tkinter.Label(self,
			anchor = "w",
			text = "Filename: "
		)
		lbl_filename.grid(
			column = 0, row = 0, columnspan = 2,
			sticky = "ew",
			padx = 10, pady = 10
		)

		# Entry for filename
		self.ent_filename = Tkinter.Entry(self)
		self.ent_filename.grid(
			column = 2, row = 0,
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
			column = 3, row = 0,
			padx = 10, pady = 10
		)

		# Button to solve the maze
		btn_solve = Tkinter.Button(self,
			text = "Solve maze!",
			width = 30,
			command = self.btn_solve_on_click
		)
		btn_solve.grid(
			column = 0, row = 1, columnspan = 4,
			padx = 10, pady = 10
		)


	def ent_filename_on_enter(self, event):
		self.btn_import_on_click()


	def btn_import_on_click(self):
		# Loading image from file
		try:
			self.img = imgloader.ImageLoader(self.ent_filename.get())
		except:
			tkMessageBox.showerror("Error", "File not found!")
			return

		# Creating graph
		self.grp = graph.Graph(self.img.pixel_map, self.img.h, self.img.w)
		tkMessageBox.showinfo("Info", "Maze successfully imported!")


	def btn_solve_on_click(self):
		# Creating new solver using DFS
		dfs_solver = dfs.DFS(self.grp)
		# Traversing the graph and getting traverse node path
		path, steps = dfs_solver.solve()
		if len(path) == 0:		# FIXME MILANA
			tkMessageBox.showerror("Error", "Maze not solved!")
			return
		# Creating new image writer so we can write our new image to the file
		iw = imgwriter.ImageWriter(self.img.mode, self.img.pixel_map, (self.img.w, self.img.h))
		# Applying path to image module
		iw.apply_path(path, self.img.pixel_map, (self.img.w, self.img.h))
		# Writing our image to output file
		iw.write("new.bmp")

		tkMessageBox.showinfo("Info", "Solved the maze in " + str(steps) + " steps!")
