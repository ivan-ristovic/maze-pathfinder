import Tkinter
import os, sys
import gui

if __name__ == "__main__":
	app = gui.Application(None)
	app.title("Maze Pathfinder")

	# Window icon setup
	parent_dir, curr_dir = os.path.split(os.getcwd())
	icon_path = os.path.join(parent_dir, "assets")
	if sys.platform.startswith('linux'):
		icon_path = os.path.join(icon_path, "icon.png")
		img = Tkinter.PhotoImage(file=icon_path)
		app.tk.call('wm', 'iconphoto', app._w, img)
	else:
		icon_path = os.path.join(icon_path, "icon.ico")
		app.iconbitmap(os.path.abspath(icon_path))

	# Starting main program loop
	app.mainloop()
