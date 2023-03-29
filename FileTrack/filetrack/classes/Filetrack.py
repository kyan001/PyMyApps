import os
import socket
import pathlib
import datetime

import consoleiotools as cit
import consolecmdtools as cct


class Trackfile:
    __version__ = "1.3.1"

    def __init__(
            self,
            trackfile_dir: str = cct.get_dir(cct.get_dir(__file__)),
            prefix: str = "TrackFile-",
            format: str = "json",
            host: bool = True):
        """
        Args:
            format: "json", "toml"
        """
        self.prefix = prefix
        self.trackfile_dir = trackfile_dir
        self.host = host
        self.hostname = socket.gethostname().replace("-", "").replace(".", "")
        self.format = format
        if self.format.upper() == "TOML":
            import tomlkit  # lazyload
            self.suffix = ".toml"
            self.formatter = tomlkit
        elif self.format.upper() == "JSON":
            import json  # lazyload
            self.suffix = ".json"
            self.formatter = json
        else:
            raise Exception(f"Output format `{self.format}` does not support")
        self.trackings = {}

    def __str__(self) -> str:
        return self.path

    @property
    def files(self) -> list[str]:
        trackfile_list = []
        for filename in os.listdir(self.trackfile_dir):
            if filename.startswith(self.prefix) and filename.endswith(self.suffix):
                if self.host and (self.hostname not in filename):
                    continue
                trackfile_list.append(filename)
        return sorted(trackfile_list)

    @property
    def latest(self) -> str:
        if not self.files:
            return None
        return self.files[-1]

    @property
    def path(self):
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        badge_hostname = f"-{self.hostname}" if self.host else ""
        return self.prefix + now + badge_hostname + self.suffix

    @staticmethod
    def diffs(trackings1: dict, trackings2: dict) -> tuple[list, list]:
        set1 = set(trackings1.items())
        set2 = set(trackings2.items())
        return [filename for filename, filehash in set1 - set2], [filename for filename, filehash in set2 - set1]

    @cit.as_session
    def save(self):
        with open(self.path, "w", encoding="UTF8") as f:
            kwargs = {}
            if self.format == "JSON":
                kwargs = {
                    "indent": 4,
                    "ensure_ascii": False
                }
            f.write(self.formatter.dumps(self.trackings, **kwargs))
            cit.info(f"New TrackFile generated: {self.path}")

    @cit.as_session
    def cleanup(self):
        if len(self.files) > 1:
            old_trackfiles = sorted(self.files)[:-1]
            cit.ask("Cleanup old TrackFiles?")
            cit.echo(old_trackfiles)
            if cit.get_choice(["Yes", "No"]) == "Yes":
                for filename in old_trackfiles:
                    abspath = os.path.abspath(filename)
                    os.remove(abspath)
                cit.info("Cleanup done")
            else:
                cit.warn("Cleanup canceled")

    @cit.as_session
    def parse(self, path: str) -> dict or None:
        if not path:
            return None
        if not os.path.isfile(path):
            raise Exception(f"TrackFile is not a file: {path}")
        cit.info(f"Parsing TrackFile `{path}`")
        with open(path, encoding="UTF8") as f:
            trackings = self.formatter.loads(f.read())
            cit.info(f"{len(trackings)} entries loaded")
        return trackings

    @cit.as_session
    def generate(self, base_dir: str = cct.get_dir(__file__), exts: list[str] = [], hash_mode: str = "CRC32",):
        """
        Args:
            hash_mode: "CRC32", "MD5", "NAME", "PATH", "MTIME"
        """
        paths = []
        for ext in exts:
            target_file_pattern = f"*.{ext}"
            cit.info(f"Target file pattern: {target_file_pattern}")
            paths += list(pathlib.Path(base_dir).rglob(target_file_pattern))
        for filepath in cit.track(paths, "Hashing...", unit="files"):
            if hash_mode == "CRC32":
                filehash = cct.crc32(filepath)
            elif hash_mode == "MTIME":
                filehash = int(os.path.getmtime(filepath))
            elif hash_mode == "NAME":
                filehash = os.path.basename(filepath)
            elif hash_mode == "PATH":
                filehash = filepath
            elif hash_mode == "MD5":
                filehash = cct.md5(filepath)
            else:
                filehash = None
            self.trackings[os.path.basename(filepath)] = filehash
