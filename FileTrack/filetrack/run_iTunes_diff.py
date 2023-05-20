import os
import unicodedata
import platform

import consoleiotools as cit
import consolecmdtools as cct

from classes import Filetrack
Filetrack.dont_write_bytecode = True
from classes import ItunesLib
ItunesLib.dont_write_bytecode = True

__version__ = "2.2.2"

BASE_DIR = cct.get_dir(cct.get_dir(__file__))
ITUNESLIB_PATH = os.path.join(BASE_DIR, "资料库.xml" if platform.system() == "Darwin" else "iTunes Library.xml")


def read_trackfile(ft: Filetrack) -> list[str]:
    old_trackings = ft.parse(ft.latest)
    if not old_trackings:
        cit.err("TrackFile unable to load.")
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


def main():
    cit.info(f"VERSION: {__version__}")
    cit.info(f"iTunes Library File: `{ITUNESLIB_PATH}`")
    cit.info(f"Update iTunes Library File by iTunes -> File -> Lib -> Export")
    trackfile = Filetrack.Trackfile()
    filetrack_songs = read_trackfile(trackfile)
    ituneslib = ItunesLib.ItunesLib(ITUNESLIB_PATH)
    show_file_only(check_diffs(checkees=filetrack_songs, checklist=ituneslib.songs))
    show_itunes_only(check_diffs(checkees=ituneslib.songs, checklist=filetrack_songs))
    cit.pause()


if __name__ == "__main__":
    cit.panel(f"[dim]{__file__}", title="[yellow]Run iTunes Diff")
    main()
