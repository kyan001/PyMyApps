from __future__ import annotations

import os
import sys
import pathlib
import socket
import datetime

import tqdm
import fuzzyfinder
import consolecmdtools as cct
import consoleiotools as cit

__version__ = '1.11.0'

BASE_DIR = cct.get_dir(__file__)
HOSTNAME = socket.gethostname().replace("-", "").replace(".", "")

TARGET_EXTS = ["mp3", "m4a"]
TRACKFILE_PREFIX = "TrackFile-"
TRACKFILE_FORMAT = "JSON"
if TRACKFILE_FORMAT == "TOML":
    import tomlkit  # lazyload
    formatter = tomlkit
    TRACKFILE_SUFFIX = ".toml"
elif TRACKFILE_FORMAT == "JSON":
    import json  # lazyload
    formatter = json
    TRACKFILE_SUFFIX = ".json"
else:
    raise Exception(f"Output format `{TRACKFILE_FORMAT}` does not support.")
HASH_MODE = "CRC32"  # "CRC32", "MD5", "NAME", "PATH", "MTIME"
SEPARATE_HOST = True


def get_trackfiles(dir: str = BASE_DIR, prefix: str = TRACKFILE_PREFIX, suffix: str = TRACKFILE_SUFFIX, separate_host: bool = SEPARATE_HOST, hostname: str = HOSTNAME) -> list[str]:
    trackfiles = []
    for fname in os.listdir(dir):
        if fname.startswith(prefix) and fname.endswith(suffix):
            if separate_host and (hostname not in fname):
                continue
            trackfiles.append(fname)
    return sorted(trackfiles)


def get_latest_trackfile() -> str:
    trackfiles = get_trackfiles()
    if not trackfiles:
        cit.warn("No TrackFile found. Ignored.")
        return None
    return trackfiles[-1]


@cit.as_session
def parse_trackfile(trackfile: str = None) -> list[str]:
    if len(sys.argv) > 1:
        input_fname = os.path.basename(sys.argv[1])
        trackfile = os.path.join(BASE_DIR, input_fname)
        cit.info(f"Input TrackFile: {input_fname}")
    if not trackfile:
        cit.err("No TrackFile input.")
        return None
    if not os.path.isfile(trackfile):
        cit.err(f"TrackFile is not a file: {trackfile}")
        return None
    cit.info(f"Parsing TrackFile `{trackfile}`")
    with open(trackfile, encoding="UTF8") as f:
        trackings = formatter.loads(f.read())
        cit.info(f"{len(trackings)} entries loaded")
        return trackings


@cit.as_session
def generate_trackings() -> dict:
    trackings = {}
    paths = []
    for ext in TARGET_EXTS:
        target_file_pattern = f"*.{ext}"
        cit.info(f"Target file pattern: {target_file_pattern}")
        paths += list(pathlib.Path(BASE_DIR).rglob(target_file_pattern))
    for fpath in tqdm.tqdm(paths, total=len(paths), unit=" files"):
        if HASH_MODE == "CRC32":
            fhash = cct.crc32(fpath)
        elif HASH_MODE == "MTIME":
            fhash = int(os.path.getmtime(fpath))
        elif HASH_MODE == "NAME":
            fhash = os.path.basename(fpath)
        elif HASH_MODE == "PATH":
            fhash = fpath
        elif HASH_MODE == "MD5":
            fhash = cct.md5(fpath)
        else:
            fhash = None
        trackings[os.path.basename(fpath)] = fhash
    return trackings


@cit.as_session
def save_new_trackfile(new_list: dict):
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    badge_hostname = f"-{HOSTNAME}" if SEPARATE_HOST else ""
    new_filetrack_filename = TRACKFILE_PREFIX + now + badge_hostname + TRACKFILE_SUFFIX
    with open(new_filetrack_filename, 'w', encoding="UTF8") as f:
        kwargs = {}
        if TRACKFILE_FORMAT == "JSON":
            kwargs = {
                "indent": 4,
                "ensure_ascii": False
            }
        f.write(formatter.dumps(new_list, **kwargs))
        cit.info(f"New TrackFile generated: {new_filetrack_filename}")
    cleanup_old_trackfiles()


def dict_diffs(dict1, dict2) -> tuple[list, list]:
    set1 = set(dict1.items())
    set2 = set(dict2.items())
    return [filename for filename, filehash in set1 - set2], [filename for filename, filehash in set2 - set1]


@cit.as_session
def cleanup_old_trackfiles():
    trackfiles = get_trackfiles()
    if len(trackfiles) > 1:
        old_trackfiles = sorted(trackfiles)[:-1]
        cit.ask("Cleanup old TrackFiles?")
        cit.echo(old_trackfiles)
        if cit.get_choice(['Yes', 'No']) == 'Yes':
            for filename in old_trackfiles:
                abspath = os.path.abspath(filename)
                os.remove(abspath)
            cit.info("Cleanup done.")
        else:
            cit.warn("Cleanup canceled.")


def main():
    cit.info(f"Version: {__version__}")
    cit.info(f"BASE_DIR: {BASE_DIR}")
    cit.info(f"HOSTNAME: {HOSTNAME}")
    latest_trackfile = get_latest_trackfile()
    old_trackings = parse_trackfile(latest_trackfile)
    new_trackings = generate_trackings()
    if old_trackings and new_trackings:
        entries_deleted, entries_added = dict_diffs(old_trackings, new_trackings)
        if entries_deleted or entries_added:
            cit.info("Changes since last time:")
            for filename in entries_deleted:
                cit.echo(filename, pre="-")
                if entries_added:
                    fuzzy = list(fuzzyfinder.fuzzyfinder(filename, entries_added))
                    if len(fuzzy) > 0:
                        cit.echo(fuzzy[0], pre="+")
                        entries_added.remove(fuzzy[0])
            for filename in entries_added:
                cit.echo(filename, pre="+")
            save_new_trackfile(new_trackings)
        else:
            cit.info("No changes")
    else:
        cit.info("Done")
        save_new_trackfile(new_trackings)
    cit.pause()


if __name__ == '__main__':
    main()
