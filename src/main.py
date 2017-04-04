import Tkinter
import sys
import gui
import filepath

if __name__ == "__main__":
	app = gui.Application(None)
	app.title("Maze Pathfinder")

	# Window icon setup
	if sys.platform.startswith('linux'):
		img = Tkinter.PhotoImage(file=filepath.get_filepath("assets", "icon.png"))
		app.tk.call('wm', 'iconphoto', app._w, img)
	else:
		app.iconbitmap(os.path.abspath(filepath.get_filepath("assets", "icon.ico")))

	# Starting main program loop
	app.mainloop()
