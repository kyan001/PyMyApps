import os
import unicodedata
import platform
import json

import consoleiotools as cit
import consolecmdtools as cct

from classes import ItunesLib


__version__ = "3.0.0"


BASE_DIR = os.path.join(cct.get_path(__file__).parent.parent.parent, "iTunesLibrary")
ITUNESLIB_PATH = os.path.join(BASE_DIR, "资料库.xml" if platform.system() == "Darwin" else "iTunes Library.xml")
TRACKFILE_DIR = cct.get_path(__file__).parent


def read_trackfile(trackfile_path: str) -> list:
    with open(trackfile_path, "r") as fl:
       old_trackings = json.load(fl)
    if not old_trackings:
        cit.err("TrackFile unable to load.")
        cit.bye()
    return [filename_purify(fname) for fname, fhash in old_trackings.items()]


def check_diffs(checkees: list, checklist: list) -> list:
    return [item for item in checkees if item not in checklist]


@cit.as_session
def show_itunes_only(diffs: list):
    cit.info(f"{len(diffs)} songs in iTunes but not in File:")
    for item in diffs:
        cit.echo(f"♬ {item}")


@cit.as_session
def show_file_only(diffs: list):
    cit.info(f"{len(diffs)} songs in File but not in iTunes:")
    for item in diffs:
        cit.echo(f"📁 {item}")


def filename_purify(name: str) -> str:
    name = os.path.splitext(name)[0]
    name = name.replace('_', '?')  # Love is _ -> Love is ?
    # import re
    # replacements = [
    #     (r'^\d\d ', ''),  # 01
    #     (r'^\d-\d\d ', ''),  # 1-01
    # ]
    # for pattern, sub in replacements:
    #     name = re.sub(pattern, sub, name)
    name = unicodedata.normalize("NFC", name)  # compressed form of Japanese chars.
    return name


def get_latest_trackfile() -> str:
    def trackfile_filter(path: str) -> bool:
        filename = cct.get_path(path).basename
        if filename.startswith(trackfile_prefix) and filename.endswith(trackfile_suffix):
            return True
        return False

    trackfile_prefix = "FileTrack-"
    trackfile_suffix = ".json"
    trackfiles = cct.get_paths(TRACKFILE_DIR, filter=trackfile_filter)
    return sorted(trackfiles)[-1] if trackfiles else ""


def main():
    cit.info(f"VERSION: {__version__}")
    cit.info(f"iTunes Library File: `{ITUNESLIB_PATH}`")
    cit.info("Update iTunes Library File by iTunes -> File -> Lib -> Export")
    latest_trackfile = get_latest_trackfile()
    filetrack_songs = read_trackfile(latest_trackfile)
    ituneslib = ItunesLib.ItunesLib(ITUNESLIB_PATH)
    show_file_only(check_diffs(checkees=filetrack_songs, checklist=ituneslib.songs))
    show_itunes_only(check_diffs(checkees=ituneslib.songs, checklist=filetrack_songs))


if __name__ == "__main__":
    cit.panel(f"[dim]{__file__}", title="[yellow]Run iTunes Diff")
    main()
    cit.pause()
