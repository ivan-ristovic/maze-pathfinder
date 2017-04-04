import os

# Get absolute file path based on folder and filename
def get_filepath(folder, filename):
	parent_dir, curr_dir = os.path.split(os.getcwd())
	folder_path = os.path.join(parent_dir, folder)
	return os.path.join(folder_path, filename)
