import Tkinter

import imgloader
import imgwriter
import graph


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
		lbl_filename = Tkinter.Label(self, anchor = "w", text = "Filename: ")
		lbl_filename.grid(column = 0, row = 0, columnspan = 2, sticky = "ew")
		# Entry for filename
		self.ent_filename = Tkinter.Entry(self)
		self.ent_filename.grid(column = 2, row = 0, sticky = "ew")
		self.ent_filename.bind("<Return>", self.ent_filename_on_enter)
		# Button to load image from file
		btn_import = Tkinter.Button(self, text = "Import maze!", command = self.btn_import_on_click)
		btn_import.grid(column = 3, row = 0)
		# Button to solve the maze
		btn_solve = Tkinter.Button(self, text = "Solve maze!", command = self.btn_solve_on_click)
		btn_solve.grid(column = 0, row = 1, columnspan = 3)
		# Info Label
		self.lbl_info = Tkinter.Label(self, anchor = "w", text = "")
		self.lbl_info.grid(column = 0, row = 2, columnspan = 3, sticky = "ew")


	def ent_filename_on_enter(self, event):
		self.btn_import_on_click()


	def btn_import_on_click(self):
		try:
			self.img = imgloader.ImageLoader(self.ent_filename.get())
			self.img.show()
			self.grp = graph.Graph(self.img.pixel_map, self.img.h, self.img.w)
			self.grp.show()
		except:
			self.lbl_info = "File not found!"


	def btn_solve_on_click(self):
		iw = imgwriter.ImageWriter(self.img.mode, self.img.pixel_map, (self.img.w, self.img.h))
		iw.write("out.bmp")
