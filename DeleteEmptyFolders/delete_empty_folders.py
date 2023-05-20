import os
import shutil

import consoleiotools as cit
import consolecmdtools as cct

__version__ = "1.0.0"


class EmptyFolderDeleter:
    IGNORE_FOLDERS = {"Base"}

    def __init__(self, base_dir: str = cct.get_dir(__file__)):
        self.base_dir = base_dir
        self.folders = []
        self.empty_folders = []
        self.ignored_folders = []
        self.delete_candidates = []

    def scan_folders(self):
        files_and_folders = os.listdir(self.base_dir)
        for itm in files_and_folders:
            if os.path.isdir(itm):
                self.folders.append(itm)
                if len(os.listdir(itm)) == 0:
                    self.empty_folders.append(itm)
                    if itm in self.IGNORE_FOLDERS:
                        self.ignored_folders.append(itm)
                    else:
                        self.delete_candidates.append(itm)

    @cit.as_session("Folder Statistics")
    def print_folder_stats(self):
        cit.info(f"Current Folder: {self.base_dir}")
        cit.info(f"Total Folders: {len(self.folders)}")
        cit.info(f"Empty Folders: {len(self.empty_folders)}")
        cit.info(f"Ignored Folders: {len(self.ignored_folders)}")
        cit.info(f"Deleted Candidates: {len(self.delete_candidates)}")

    @cit.as_session("Folder List")
    def print_folder_list(self):
        for folder in self.folders:
            flag = ""
            if folder in self.ignored_folders:
                flag = " [yellow]-> Ignored"
            if folder in self.delete_candidates:
                flag = " [red]-> Removed"
            if folder not in self.empty_folders:
                flag = " [dim]Not Empty"
            cit.info(f"{folder}{flag}")

    def delete_empty_folders(self):
        if cit.get_input(f"[u]{len(self.delete_candidates)}[/] of the folders will be removed, is that OK?", default="Yes") == "Yes":
            for folder in self.delete_candidates:
                shutil.rmtree(os.path.join(self.base_dir, folder))
            cit.info(f"{len(self.delete_candidates)} folders removed.")
        else:
            cit.warn("Delete cancelled.")


if __name__ == '__main__':
    efr = EmptyFolderDeleter()
    efr.scan_folders()
    efr.print_folder_list()
    efr.print_folder_stats()
    efr.delete_empty_folders()
