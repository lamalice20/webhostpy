import shutil 
import os

path_to_copy_files_and_create_folders = "C:\\webhostpy\\"

if os.path.exists(path_to_copy_files_and_create_folders):
	pass
else:
	os.makedirs(path_to_copy_files_and_create_folders)

shutil.copy("running.py", path_to_copy_files_and_create_folders)
shutil.copy("requirements.txt", path_to_copy_files_and_create_folders)
shutil.copy("README.md", path_to_copy_files_and_create_folders)

os.makedirs(f"{path_to_copy_files_and_create_folders}\\UpdateFolder\\")

