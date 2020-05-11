#!.pyenv/versions/3.8.2/bin/python3.8
'''
To be used as a crontask

Scans downloads folder, moves certain file types into folders automatically

On newer macos (definitely Catalina) will need to grant cron Full Disc Access
'''
import os
import pathlib
import shutil
import time


# Set how long new files live in Downloads before being sorted
do_not_move_for = 30

# Which folders to put which file type in
# Add filetypes (keys) or folders (values) to add sorting features
# Extensions not found in this dict go into a folder called "other"
ext_to_folders = {
    ".doc": "Docs",
    ".docx": "Docs",
    ".txt": "Docs",
    ".xls": "Docs",
    ".xlsx": "Docs",
    ".gif": "Images",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".JPG": "Images",
    ".png": "Images",
    ".psd": "Images",
    ".tif": "Images",
    ".tiff": "Images",
    ".mp4": "Music and Movies",
    ".mp3": "Music and Movies",
    ".pdf": "PDFs",
    ".bz2": "System",
    ".dmg": "System",
    ".pkg": "System",
    ".tz": "System",
    ".zip": "System",
}

# Location of the downloads folder
download_folder_path = os.path.expanduser('~/Downloads')

# Collects files into a list
list_of_files = os.listdir(download_folder_path)


# The current time
current_epoch_time = time.time()


# For each file in the downloads folder
for file in list_of_files:

    # Skips to next file if file is actualy a dir
    # This leaves the current any folders in /Downloads
    if os.path.isdir(download_folder_path + '/' + file) == True:
        continue

    # Creates object of file data (ex: file created, last modified)
    # Docs: https://docs.python.org/3/library/os.html#os.stat
    file_stats = os.stat(download_folder_path+'/'+file)

    # Gets file creation time to nearest second
    file_creation_time = round(file_stats.st_birthtime)

    if file_creation_time + 60 * do_not_move_for < current_epoch_time:
        # The extension of the given file ('' if no extension or folder)
        ext = pathlib.Path(file).suffix

        # If the extension is in the ext_to_folders Dict
        if ext in ext_to_folders.keys():
            # If the desitation folder doesn't exist, make it
            if not os.path.exists(download_folder_path+'/'+ext_to_folders[ext]):
                os.makedirs(download_folder_path+'/'+ext_to_folders[ext])
            # Move the file to the appropriate folder
            shutil.move(
                download_folder_path + '/' + file,
                download_folder_path + '/' + ext_to_folders[ext] + '/' + file)

        # Files without extensions or
        # where extensions are not in ext_to_folders Dict
        else:
            if not os.path.exists(download_folder_path+'/other'):
                os.makedirs(download_folder_path+'/other')
            # Move the file to the appropriate folder
            shutil.move(
                download_folder_path + '/' + file,
                download_folder_path + '/other/' + file)
