import Tkinter

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

		# Info Label
		self.lbl_info = Tkinter.Label(self,
			anchor = "w",
			fg = "red",
			text = ""
		)
		self.lbl_info.grid(
			column = 0, row = 2, columnspan = 4,
			sticky = "ew",
			padx = 10, pady = 10
		)


	def ent_filename_on_enter(self, event):
		self.btn_import_on_click()


	def btn_import_on_click(self):
		# Loading image from file
		try:
			self.img = imgloader.ImageLoader(self.ent_filename.get())
		except:
			self.lbl_info.config(text = "File not found!")
			return

		self.lbl_info.config(text = "")
		self.img.show()		# TODO remove

		# Creating graph
		self.grp = graph.Graph(self.img.pixel_map, self.img.h, self.img.w)
		self.grp.show()		# TODO remove

	def btn_solve_on_click(self):
		iw = imgwriter.ImageWriter(self.img.mode, self.img.pixel_map, (self.img.w, self.img.h))
		iw.write("out.bmp")
		dfsSolver = dfs.DFS(self.grp)
		dfsSolver.solve()

