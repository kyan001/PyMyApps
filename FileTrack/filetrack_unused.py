import os
import plistlib
import re
import unicodedata

import consoleiotools as cit

import filetrack_changed

__version__ = "1.0.0"

ITUNES_LIBRARY_FILE = "资料库.xml" if os.path.isfile("资料库.xml") else "iTunes Library.xml"


def read_itunes_library(lib_file: str = None) -> list[str]:
    lib_file = lib_file or ITUNES_LIBRARY_FILE
    itunes_library_list = []
    with open(lib_file, 'rb') as f:
        tracks = plistlib.load(f)['Tracks']
    for id in tracks:
        name = tracks[id]['Name']
        track_num = tracks[id].get('Track Number')
        disc_num = tracks[id].get('Disc Number')
        if track_num is not None:
            if disc_num is not None:
                itunes_library_list.append(f"{disc_num}-{track_num:0>2} {name}")
            else:
                itunes_library_list.append(f"{track_num:0>2} {name}")
        else:
            itunes_library_list.append(name)
    return itunes_library_list


def read_trackfile() -> list[str]:
    latest_trackfile = filetrack_changed.get_latest_trackfile()
    trackings = filetrack_changed.parse_trackfile(latest_trackfile)
    if not trackings:
        cit.err("TrackFile unable to load.")
    return [filename_purify(fname) for fname, fhash in trackings.items()]


def check_diffs(checkees: list, checklist: list) -> list:
    return [item for item in checkees if item not in checklist]


@cit.as_session
def show_itunes_only(diffs: list):
    cit.info(f"{len(diffs)} songs in iTunes but not in File:")
    cit.info(f"(Update {ITUNES_LIBRARY_FILE} using iTunes -> File -> Lib -> Export)")
    for item in diffs:
        cit.echo(f"{item}")


@cit.as_session
def show_file_only(diffs: list):
    cit.info(f"{len(diffs)} songs in File but not in iTunes:")
    for item in diffs:
        cit.echo(f"{item}")


def filename_purify(name: str) -> str:
    name = os.path.splitext(name)[0]
    replacements = [
        # (r'^\d\d ', ''),  # 01
        # (r'^\d-\d\d ', ''),  # 1-01
        (r'_', '?'),  # Love is _ -> Love is ?
    ]
    for pattern, sub in replacements:
        name = re.sub(pattern, sub, name)
    name = unicodedata.normalize("NFC", name)  # compressed form of Japanese chars.
    return name


def main():
    filetrack_songs = read_trackfile()
    itunes_lib_songs = read_itunes_library()
    show_itunes_only(check_diffs(checkees=filetrack_songs, checklist=itunes_lib_songs))
    show_file_only(check_diffs(checkees=itunes_lib_songs, checklist=filetrack_songs))


if __name__ == "__main__":
    main()
