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

__version__ = '1.10.1'

BASE_DIR = cct.get_dir(__file__)
HOSTNAME = socket.gethostname().replace("-", "").replace(".", "")

TARGET_FILE_PATTERN = "*.mp3"
LISTFILE_PREFIX = TARGET_FILE_PATTERN.split(".")[-1] + "list-"
OUTPUT_FORMAT = "JSON"
if OUTPUT_FORMAT == "TOML":
    import tomlkit
    formatter = tomlkit
    LISTFILE_SUFFIX = ".toml"
elif OUTPUT_FORMAT == "JSON":
    import json
    formatter = json
    LISTFILE_SUFFIX = ".json"
else:
    raise Exception(f"OUTPUT_FORMAT {FORMAT} does not support.")
HASH_MODE = "CRC32"  # "CRC32", "MD5", "NAME", "PATH", "MTIME"
SEPARATE_HOST = True


def get_old_list_files() -> list[str]:
    list_files = []
    for filename in os.listdir(BASE_DIR):
        if filename.startswith(LISTFILE_PREFIX) and filename.endswith(LISTFILE_SUFFIX):
            if SEPARATE_HOST and (HOSTNAME not in filename):
                continue
            list_files.append(filename)
    return sorted(list_files)


@cit.as_session
def read_old_list_file() -> list[str]:
    if len(sys.argv) > 1:
        input_file = os.path.basename(sys.argv[1])
        old_list_file = os.path.join(BASE_DIR, input_file)
        cit.info(f"Input file: {input_file}")
    else:
        old_list_files = get_old_list_files()
        old_list_file = old_list_files[-1] if old_list_files else None
    if not old_list_file:
        cit.warn("Old list file does not found, ignored.")
    elif not os.path.isfile(old_list_file):
        cit.err(f"Old list file is not a file: {old_list_file}")
    else:
        cit.info(f"Old list file: {old_list_file}")
        with open(old_list_file, encoding="UTF8") as f:
            old_list = formatter.loads(f.read())
            cit.info(f"{len(old_list)} entries loaded")
            return old_list
    return None


@cit.as_session
def generate_new_list() -> dict:
    file_hashes = {}
    cit.info(f"Target files pattern: {TARGET_FILE_PATTERN}")
    pathlist = list(pathlib.Path(BASE_DIR).rglob(TARGET_FILE_PATTERN))
    for fpath in tqdm.tqdm(pathlist, total=len(pathlist), unit=" files"):
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
        file_hashes[os.path.basename(fpath)] = fhash
    return file_hashes


@cit.as_session
def save_new_list(new_list: dict):
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    hostname_badge = f"-{HOSTNAME}" if SEPARATE_HOST else ""
    new_list_filename = LISTFILE_PREFIX + now + hostname_badge + LISTFILE_SUFFIX
    with open(new_list_filename, 'w', encoding="UTF8") as f:
        kwargs = {}
        if OUTPUT_FORMAT == "JSON":
            kwargs = {
                "indent": 4,
                "ensure_ascii": False
            }
        f.write(formatter.dumps(new_list, **kwargs))
        cit.info(f"New list file generated: {new_list_filename}")
    clean_up_old_list_files()


def dict_diffs(dict1, dict2) -> tuple[list, list]:
    set1 = set(dict1.items())
    set2 = set(dict2.items())
    return [filename for filename, filehash in set1 - set2], [filename for filename, filehash in set2 - set1]


@cit.as_session
def clean_up_old_list_files():
    list_files = get_old_list_files()
    if len(list_files) > 1:
        old_list_files = sorted(list_files)[:-1]
        cit.ask("Clean up old list files?")
        cit.echo(old_list_files)
        if cit.get_choice(['Yes', 'No']) == 'Yes':
            for filename in old_list_files:
                abspath = os.path.abspath(filename)
                os.remove(abspath)
            cit.info("Clean up done.")
        else:
            cit.warn("Clean up canceled.")


def main():
    cit.info(f"Version: {__version__}")
    cit.info(f"BASE_DIR: {BASE_DIR}")
    cit.info(f"HOSTNAME: {HOSTNAME}")
    old_list = read_old_list_file()
    new_list = generate_new_list()
    if old_list and new_list:
        diffs_del, diffs_add = dict_diffs(old_list, new_list)
        if diffs_del or diffs_add:
            cit.info("Changes since last time:")
            for filename in diffs_del:
                cit.echo(filename, pre="-")
                if diffs_add:
                    fuzzy = fuzzyfinder.fuzzyfinder(filename, diffs_add)
                    fuzzy_list = list(fuzzy)
                    if len(fuzzy_list) > 0:
                        cit.echo(fuzzy_list[0], pre="+")
                        diffs_add.remove(fuzzy_list[0])
            for filename in diffs_add:
                cit.echo(filename, pre="+")
            save_new_list(new_list)
        else:
            cit.info("No changes")
    else:
        cit.info("Done")
        save_new_list(new_list)
    cit.pause()


if __name__ == '__main__':
    main()
