import os
import sys
import pathlib
import json
import socket
import datetime

import tqdm
import consolecmdtools as cct
import consoleiotools as cit

__version__ = '1.5.1'

BASE_DIR = cct.get_dir(__file__)
HOSTNAME = socket.gethostname()

TARGET_FILE_PATTERN = "*.mp3"
LISTFILE_PREFIX = TARGET_FILE_PATTERN.split(".")[-1] + "list-"
LISTFILE_SUFFIX = ".json"
HASH_MODE = "CRC32"  # "CRC32", "MD5", "NAME", "PATH", "MTIME"
SEPARATE_HOST = True


def get_old_list_files() -> list:
    list_files = []
    for filename in os.listdir(BASE_DIR):
        if filename.startswith(LISTFILE_PREFIX) and filename.endswith(LISTFILE_SUFFIX):
            if SEPARATE_HOST and (HOSTNAME not in filename):
                continue
            list_files.append(filename)
    return list_files


@cit.as_session
def read_old_list_file():
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
            old_list = json.loads(f.read())
            cit.info(f"{len(old_list)} entries loaded")
            return old_list
    return None


@cit.as_session
def generate_new_list():
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
        f.write(json.dumps(new_list, indent=4, ensure_ascii=False))
        cit.info(f"New list file generated: {new_list_filename}")
    clean_up_old_list_files()


def dict_diffs(dict1, dict2):
    return set(dict1.items()) ^ set(dict2.items())


@cit.as_session
def clean_up_old_list_files():
    list_files = get_old_list_files()
    if len(list_files) > 1:
        old_list_files = list_files[:-1]
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
        diffs = dict_diffs(old_list, new_list)
        if diffs:
            cit.info("Changes since last time:")
            for filename, hash in diffs:
                cit.echo(filename)
            save_new_list(new_list)
        else:
            cit.info("No changes")
    else:
        cit.info("Done")
        save_new_list(new_list)
    cit.pause()


if __name__ == '__main__':
    main()
