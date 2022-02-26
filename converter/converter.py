import os
import pathlib
import time

import pandas as pd

SOURCE_PATH = pathlib.Path("\\\\JM-HOME-SERVER\\aini record - batch 01\\MASTER - VCD")
TARGET_PATH = pathlib.Path("\\\\JM-HOME-SERVER\\aini record - batch 01\\MASTER - MP4")

if not pathlib.Path("log").exists():
    os.mkdir("log")

def get_tracks(path):
    tracks = []
    for album in os.listdir(path):
        album_path = path / album
        for volume in os.listdir(album_path):
            volume_path = album_path / volume
            for track in os.listdir(volume_path):
                track_path = volume_path / track
                tracks.append(track_path)

    return tracks


if not os.path.exists(TARGET_PATH):
    os.makedirs(TARGET_PATH)

source_tracks = get_tracks(SOURCE_PATH)
target_tracks = get_tracks(TARGET_PATH)


def get_track_id(track_path):
    album_id = track_path.parent.parent.name
    album_id += track_path.parent.name
    album_id += track_path.name
    return album_id.split(".")[0]


def get_dataframe(tracks):
    df = pd.DataFrame(tracks, columns=["path"])
    df["id"] = df["path"].apply(get_track_id)
    df.set_index("id", inplace=True)
    return df


source_df = get_dataframe(source_tracks)
target_df = get_dataframe(target_tracks)

queue_df = source_df.loc[~source_df.index.isin(target_df.index)]


def convert(input, output):
    print("Converting '{}' to '{}'".format(input, output))
    if not os.path.exists(output.parent):
        os.makedirs(output.parent)
    os.system("ffmpeg -y -i \"{}\" -c:v h264_nvenc -vf scale=-1:1080 -b:v 10M \"{}\"".format(input, output))

logger = time.strftime('%H-%M-%S')

for index, row in queue_df.iterrows():
    _input = row["path"]
    output = TARGET_PATH / "\\".join(str(_input).split("\\")[-3:]).replace(".dat", ".mp4")
    with open(f"log/{logger}.txt", "a") as log:
        log.write(f"{time.strftime('%H:%M:%S')} - Converting '{_input}' to '{output}'\n")
    convert(_input, output)
