import os
import plistlib


class ItunesLib:
    __version__ = "1.0.0"

    def __init__(self, path: str = "资料库.xml"):
        self.path = path if os.path.isfile(path) else "iTunes Library.xml"

    @property
    def songs(self) -> list[str]:
        songs = []
        with open(self.path, 'rb') as f:
            tracks = plistlib.load(f)['Tracks']
        for id in tracks:
            name = tracks[id]['Name']
            track_num = tracks[id].get('Track Number')
            disc_num = tracks[id].get('Disc Number')
            if tracks[id]['Genre'] == "语音备忘录":
                print(name)
            if track_num is None:
                songs.append(name)
            elif disc_num is None:
                songs.append(f"{track_num:0>2} {name}")
            else:
                songs.append(f"{disc_num}-{track_num:0>2} {name}")
        return songs
