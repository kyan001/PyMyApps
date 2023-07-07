from __future__ import annotations

import os

import fuzzyfinder
import consolecmdtools as cct
import consoleiotools as cit

from classes import Filetrack
Filetrack.dont_write_bytecode = True

__version__ = '2.2.3'

TARGET_EXTS = ["mp3", "m4a"]
HASH_MODE = "CRC32"  # "CRC32", "MD5", "NAME", "PATH", "MTIME"
BASE_DIR = cct.get_dir(cct.get_dir(__file__))


def compare(ft: Filetrack):
    old_trackings = ft.parse(ft.latest)
    ft.generate(
        base_dir=BASE_DIR,
        exts=TARGET_EXTS,
        hash_mode=HASH_MODE
    )
    if old_trackings and ft.trackings:
        entries_deleted, entries_added = ft.diffs(old_trackings, ft.trackings)
        if entries_deleted or entries_added:
            cit.info("Changes since last time: ✍️")
            for filename in entries_deleted:
                cit.echo(filename, pre="-")
                if entries_added:
                    fuzzy = list(fuzzyfinder.fuzzyfinder(filename, entries_added))
                    if len(fuzzy) > 0:
                        cit.echo(fuzzy[0], pre="+")
                        entries_added.remove(fuzzy[0])
            for filename in entries_added:
                cit.echo(filename, pre="+")
            ft.save()
            ft.cleanup()
        else:
            cit.info("No changes")
    else:
        cit.info("Done")
        ft.save()
        ft.cleanup()


def main():
    ft = Filetrack.Trackfile(
        trackfile_dir=cct.get_dir(__file__),
        prefix="TrackFile-",
        format="json",
        host=True,
    )
    cit.info(f"Version: {ft.__version__}")
    cit.info(f"Trackfile Dir: 📂 {ft.trackfile_dir}")
    cit.info(f"Target File Folder: 📂 {BASE_DIR}")
    cit.info(f"Hash Mod: 🧮 {HASH_MODE}")
    cit.info(f"Target Extensions: 📜 {TARGET_EXTS}")
    cit.info(f"Hostname: 💻 {ft.hostname}")
    compare(ft)
    cit.pause()


if __name__ == '__main__':
    cit.panel(f"[dim]{__file__}", title="▶ [yellow]Run Filetrack")
    main()
