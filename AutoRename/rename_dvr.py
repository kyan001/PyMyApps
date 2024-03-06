import re
import os
import tomllib

import consoleiotools as cit
import consolecmdtools as cct


__version__ = "0.0.1"
TOML_FILENAME = "rename.toml"


def parse_config(path: cct.Path) -> dict:
    if not path.is_file:
        cit.err(f"Config File not found: {path}")
        cit.bye()
    with open(path, "rb") as fl:
        return tomllib.load(fl)


def validate_filename(path: cct.Path, pattern: str):
    if re.match(pattern, path.basename):
        return True
    else:
        return False


def get_date(path: cct.Path, date_pattern: str, date_split: str):
    """Get date from file name."""
    date = re.search(date_pattern, path.basename)
    if date:
        return "".join(date.group().split(date_split))
    else:
        return None


def main():
    config = parse_config(cct.get_path(TOML_FILENAME))
    current_folder = cct.get_path(__file__).parent
    rename_count = 0
    for path in cct.bfs_walk(current_folder):
        path = cct.get_path(path)
        if path.is_file and validate_filename(path, config.get("pattern").get("name")):
            cit.info(f"Processing: {path.basename}")
            date = get_date(path, config.get("pattern").get("date"), config.get("pattern").get("split"))
            for i in range(1, 99):
                new_filename = f"{config.get("prefix")}-{date}-{i:02}.mp4"
                new_filepath = os.path.join(path.parent, new_filename)
                if not cct.get_path(new_filepath).exists:
                    cct.move_file(path, new_filepath, msgout=cit.mute)
                    cit.info(f"Renamed to: {new_filename}")
                    rename_count = rename_count + 1
                    break
            else:
                cit.warn("Too many files with the same date.")
    cit.info(f"Renamed {rename_count} files.")


if __name__ == '__main__':
    main()
    cit.pause()
