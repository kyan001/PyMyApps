import os
import pathlib

import tomlkit
import consolecmdtools as cct
import consoleiotools as cit

__version__ = '1.2.2'


def get_root_folder(config_path: str = os.path.splitext(cct.get_path(__file__))[0] + ".toml") -> str:
    if os.path.isfile(config_path):
        with open(config_path, "r") as f:
            config = tomlkit.parse(f.read())
            if config and config.get("folder"):
                base_dir = cct.get_path(__file__, parent=True)
                relative_path = os.path.join(base_dir, config["folder"])
                return cct.get_path(relative_path)
    return cct.get_path(__file__, parent=True)  # default to the folder of this script


def is_empty(path):
    """Check if a given path is an empty folder

    Args:
        path (str): path to check

    Returns:
        bool: True if the path is an empty folder, False if it is not an empty folder, None if the path is a file or does not exist
    """
    if not os.path.exists(path):
        return None
    if os.path.isfile(path):
        return None
    for root, dirs, files in os.walk(path):
        if files:  # return False if any files are found
            return False
        if dirs:  # return False if any of the subfolders is not empty
            for dir in dirs:
                if not is_empty(os.path.join(root, dir)):
                    return False
    return True

def has_empty(path):
    """Check if a given path has empty folders"""
    if not os.path.exists(path):
        return None
    if os.path.isfile(path):
        return None
    if is_empty(path):  # return True if the path itself is an empty folder
        return True
    for root, dirs, files in os.walk(path):
        if dirs:
            for dir in dirs:
                if is_empty(os.path.join(root, dir)):  # return True if any of the subfolders is empty
                    return True
    return False


def bfs_walk(root_folder):
    queue = [pathlib.Path(root_folder)]
    while queue:
        path = queue.pop(0)
        yield path
        if path.is_dir():
            # insert into the front of the queue
            queue = [p for p in path.iterdir()] + queue


def empty_folder_tree(root_folder):
    """List folders under root_folder."""
    cit.echo(f'📂 {cct.get_path(root_folder, basename=True)}{os.sep}')
    dir_count = 0
    file_count = 0
    empty_count = 0
    for path in bfs_walk(root_folder):
        depth = len(path.relative_to(root_folder).parts)
        prefix = '|   ' * (depth - 1) + f"|--{'📂' if path.is_dir() else '📄'}"
        suffix = ' '.join([
            os.sep if path.is_dir() else '',
            '🈳' if is_empty(path) else '',
        ])
        if path.is_dir():
            dir_count += 1
        else:
            file_count += 1
        if is_empty(path):
            empty_count += 1
        if has_empty(path):
            cit.echo(f'{prefix} {path.name}{suffix}')
    cit.info(f"Total: {dir_count} folders, {file_count} files, {empty_count} empty folders.")


def main():
    root_folder = get_root_folder()
    cit.panel(f"{root_folder}", title="📂 Root Folder")
    empty_folder_tree(root_folder)

if __name__ == "__main__":
    main()
