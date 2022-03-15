import argparse
import os
import pathlib
from glob import glob

args = argparse.ArgumentParser(description='Convert a DAT file to MP4')
args.add_argument('-i', '--input', help='Input Folder file', required=True)

args = args.parse_args()

OUTPUT_PATH = f"{pathlib.Path.home()}\\Desktop\\output"

input_folder = "\\\\JM-HOME-SERVER\\Aini Record - VCD\\" + args.input
output_folder = OUTPUT_PATH + "\\" + input_folder.split('\\')[-1]
output_folder = pathlib.Path(output_folder)


print(f"Input Folder: {input_folder}")
print(f"Output Folder: {output_folder}")
if output_folder.exists():
    print("Folder already exists")
    exit()
output_folder.mkdir(parents=True)

for file in glob(input_folder + '\\*.dat'):
    print("\n")
    print('Converting: ' + file)
    filename = file.split('\\')[-1]
    filename = filename.split('.')[0]
    os.system(f"ffmpeg -y -i \"{file}\" -b:v 20M \"{output_folder}\\{filename}.mp4\" -hide_banner -loglevel panic")
    print('Converted: ' + file)
