import glob
import os
import pathlib
import shutil
import time
import tqdm
import win32api

from cloner.CONFIG import STORAGE_PATH

drives = win32api.GetLogicalDriveStrings()
drives = drives.split('\000')[:-1]

print("Drive List:")
for i, drive in enumerate(drives):
    print(f"\t{i + 1}. {drive}")

input_disk = input("Select Disk to clone: ")
input_disk = drives[int(input_disk) - 1]

folder = pathlib.Path(f"{input_disk}\\MPEGAV")


def get_file_size(file_path):
    return round(os.path.getsize(file_path) / (1024 * 1024))


files = glob.glob(f"{folder}\\*.dat")
files = [pathlib.Path(file) for file in files]

print("\n\nTable of Contents:")
for i, file in enumerate(files):
    print(f"\t{i + 1:2d}. {file.name} - {get_file_size(file):4d} MB")

input_album = input("\nInput Album ID : AR")
input_album_volume = input("Input Album Volume : ")

input_album = "AR" + input_album.zfill(4)
input_album_volume = input_album_volume.zfill(3)
target_album = pathlib.Path(f"{STORAGE_PATH}\\{input_album}")
target_album_volume = pathlib.Path(f"{STORAGE_PATH}\\{input_album}\\{input_album_volume}")

print(f"\nAlbum ID : {input_album + input_album_volume}XXX")

if target_album_volume.exists():
    # Check Target Folder is Empty
    if len(os.listdir(target_album_volume)) > 0:
        msg = "\n\n\n" + "=" * 64
        msg += "\nAlbum Already Exist\n"
        msg += f"{target_album_volume}\n"
        msg += "Please Remove The Folder And Try Again.\n"
        msg += "=" * 64
        exit(msg)
else:
    target_album_volume.mkdir(parents=True)

print(f"\nStart Cloning at {time.strftime('%H:%M:%S')}")
for i, file in tqdm.tqdm(enumerate(files), desc="Cloning Files", unit="file"):
    path = pathlib.Path(f"{target_album_volume}\\{i + 1:03d}.dat")
    shutil.copy(file, path)
