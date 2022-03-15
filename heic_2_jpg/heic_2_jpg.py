import pathlib

import PIL as pil
from glob import glob
from PIL import Image
from pillow_heif import register_heif_opener
SOURCE = "\\\\JM-HOME-SERVER\\Aini Record - VCD - Album Image\\belsa 2"
TARGET = "\\\\JM-HOME-SERVER\\Aini Record - VCD - Album Image\\belsa_2_jpg"
register_heif_opener()
pathlib.Path(TARGET).mkdir(parents=True, exist_ok=True)

files = glob(f"{SOURCE}\\*.HEIC")

for i, file in enumerate(files):
    file_name = pathlib.Path(file).name.split(".")[0]
    img = Image.open(file)
    img.save(f"{TARGET}\\{file_name}.jpg")
    print(f"{i}/{len(files)}")