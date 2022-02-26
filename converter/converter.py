import os
import path
import pandas as pd

SOURCE_PATH = path.Path("\\\\JM-HOME-SERVER\\aini record - batch 01\\MASTER - VCD")
TARGET_PATH = path.Path("\\\\JM-HOME-SERVER\\aini record - batch 01\\MASTER - MP4")


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

    # convert to mp4 and scale to 1080p
    os.system("ffmpeg -y -i \"{}\" -vf scale=-1:1080  \"{}\"".format(input, output))


for index, row in queue_df.iterrows():
    input = row["path"]
    output = TARGET_PATH / "\\".join(input.split("\\")[-3:]).replace(".dat", ".mp4")
    convert(input, output)
    break
