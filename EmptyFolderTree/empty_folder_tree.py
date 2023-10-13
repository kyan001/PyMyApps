import os
import pathlib
import shutil

import tomlkit
import consolecmdtools as cct
import consoleiotools as cit

__version__ = "1.4.1"


CONFIG = {}

def config_init(config_path: str = cct.get_path(__file__).stem + ".toml"):
    if os.path.isfile(config_path):
        config = tomlkit.parse(cct.read_file(config_path))
        if config:
            CONFIG["self"] = config_path
            CONFIG["root_folder"] = config.get("root_folder")
            CONFIG["show_files"] = config.get("show_files")
            CONFIG["show_all_folders"] = config.get("show_all_folders")
            CONFIG["ignore"] = config.get("ignore")


def get_root_folder() -> str:
    """Get the root folder to scan for empty folders"""
    if CONFIG.get("root_folder"):
        base_dir = cct.get_path(__file__).parent
        relative_path = os.path.join(base_dir, CONFIG.get("root_folder"))
        return cct.get_path(relative_path)
    return cct.get_path(__file__).parent  # default to the folder of this script


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


def traverse_empty_folder(root_folder: str) -> list[str]:
    """Traverse the folder tree and return a list of empty folders"""
    def to_visible(path: str) -> bool:
        if CONFIG.get("show_files") and path.is_file():
            return True
        if CONFIG.get("show_all_folders") and path.is_dir():
            return True
        if has_empty(path):
            return True
        return False

    def to_highlight(path: str) -> bool:
        if is_empty(path):
            return True
        return False

    def add_suffix(path: str) -> str:
        suffix = []
        if is_empty(path):
            suffix.append("🈳")
        if CONFIG.get("ignore") and path.name in CONFIG.get("ignore"):
            suffix.append("[red](IGNORED)[/]")
        return " ".join(suffix)

    def path_fitler(path: str) -> bool:
        if CONFIG.get("ignore") and path.name in CONFIG.get("ignore"):
            return False
        if is_empty(path):
            return True
        return False

    delete_candidates = cct.get_files(root_folder, filter=path_fitler)
    cct.ls_tree(root_folder, show_icon=True, to_visible=to_visible, to_highlight=to_highlight, add_suffix=add_suffix)
    return delete_candidates

def delete_empty_folders(empty_folders: list[str]):
    if empty_folders:
        if cit.get_input(f"[yellow]{len(empty_folders)}[/] of the folders will be removed, is that OK?", default="Yes") == "Yes":
            for folder in empty_folders:
                shutil.rmtree(folder)
            cit.info(f"{len(empty_folders)} folders removed.")
        else:
            cit.warn("Delete cancelled.")
    else:
        cit.info("No empty folders found.")

def main():
    config_init()
    root_folder = get_root_folder()
    info_texts = [f"📂 Root Folder: {root_folder}",]
    if CONFIG:
        info_texts.append(f"🛠️ Config File: {CONFIG.get('self')}")
        info_texts.append(f"👀 Show Files: {'✔' if CONFIG.get('show_files') else '✖'}")
        info_texts.append(f"👀 Show All Folders: {'✔' if CONFIG.get('show_all_folders') else '✖'}")
    cit.panel("\n".join(info_texts), title="Info")
    empty_folders = traverse_empty_folder(root_folder)
    delete_empty_folders(empty_folders)


if __name__ == "__main__":
    main()
    cit.pause()
