import os
import pathlib

import consolecmdtools as cct
import consoleiotools as cit

__version__ = '1.0.0'


_itunes_tools_dir = cct.get_path(__file__, parent=True)
_itunes_extras_dir = cct.get_path(_itunes_tools_dir, parent=True)
_app_folder_dir = cct.get_path(_itunes_extras_dir, parent=True)
_itunes_library_dir = os.path.join(_app_folder_dir, 'iTunesLibrary')
_itunes_media_dir = os.path.join(_itunes_library_dir, 'iTunes Media')
_itunes_music_dir = os.path.join(_itunes_media_dir, 'Music')
ROOT_FOLDER = _itunes_music_dir

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
    cit.echo(f'{root_folder}{os.sep}')
    for path in bfs_walk(root_folder):
        depth = len(path.relative_to(root_folder).parts)
        prefix = '    ' * (depth - 1) + '|-- '
        pathname = ('📂' if os.path.isdir(path) else '') + path.name
        suffix = ' '.join([
            os.sep if path.is_dir() else '',
            '🈳' if is_empty(path) else '',
        ])
        if has_empty(path):
            cit.echo(f'{prefix}{pathname}{suffix}')


def main():
    cit.panel(f"Root Folder: 📂{ROOT_FOLDER}")
    empty_folder_tree(ROOT_FOLDER)

if __name__ == "__main__":
    main()
