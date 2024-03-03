import os
import socket
import pathlib
import datetime

import consoleiotools as cit
import consolecmdtools as cct


class Trackfile:
    __version__ = "1.5.8"

    def __init__(self, trackfile_dir: str = cct.get_path(__file__).parent, prefix: str = "TrackFile-", format: str = "json", host: bool = True):
        """Initialize Trackfile object.

        Args:
            format: "json", "toml"
        """
        self.prefix = prefix
        self.trackfile_dir = trackfile_dir
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
        self.host = host
        self.hostname = self.get_hostname()
        self.trackings = {}

    def __str__(self) -> str:
        return self.path

    @property
    def hosts(self) -> list:
        """list of known hosts in trackfile_dir"""
        trackfile_list = []
        for filename in os.listdir(self.trackfile_dir):
            if filename.startswith(self.prefix) and filename.endswith(self.suffix):
                trackfile_list.append(filename.split("-")[2].split(".")[0])
        return sorted(list(set(trackfile_list)))

    @property
    def files(self) -> list:
        trackfile_list = []
        for filename in os.listdir(self.trackfile_dir):
            if filename.startswith(self.prefix) and filename.endswith(self.suffix):
                if self.host and (self.hostname not in filename):
                    continue
                trackfile_list.append(os.path.join(self.trackfile_dir, filename))
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
    def diffs(trackings1: dict, trackings2: dict) -> 'tuple[list, list]':
        set1 = set(trackings1.items())
        set2 = set(trackings2.items())
        return [filename for filename, filehash in set1 - set2], [filename for filename, filehash in set2 - set1]

    def get_hostname(self):
        """Get hostname and check if hostname is new."""
        host = socket.gethostname().replace("-", "").replace(".", "")  # default hostname
        if host not in self.hosts:
            if cit.get_input(f"New hostname `{host}` detected. Continue?", default="Yes") != "Yes":
                cit.info("Please choose a hostname from the list below:")
                return cit.get_choice(self.hosts)
        return host

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
            for trackfile in old_trackfiles:
                cit.echo(cct.get_path(trackfile).basename, pre="*")
            if cit.get_choice(["Yes", "No"]) == "Yes":
                for filepath in old_trackfiles:
                    os.remove(filepath)
                cit.info("Cleanup done")
            else:
                cit.warn("Cleanup canceled")

    @cit.as_session
    def parse(self, path: str) -> dict:
        if not path:
            return {}
        if not os.path.isfile(path):
            raise Exception(f"TrackFile is not a file: {path}")
        cit.info(f"Parsing TrackFile `{path}`")
        with open(path, encoding="UTF8") as f:
            trackings = self.formatter.loads(f.read())
            cit.info(f"{len(trackings)} entries loaded")
        return trackings

    @cit.as_session
    def generate(self, target_dir: str = cct.get_path(__file__).parent, exts: list = [], hash_mode: str = "CRC32"):
        """Generate file tracking information.

        Args:
            target_dir (str): Target directory to scan.
            exts (list[str]): Accepted file extensions. Ex. ["mp3", "m4a"]
            hash_mode (str): "CRC32", "MD5", "NAME", "PATH", "MTIME"

        Returns:
            dict: {filename: filehash}
        """
        paths = []
        for ext in exts:
            target_file_pattern = f"*.{ext}"
            cit.info(f"Target file pattern: {target_file_pattern}")
            paths += list(pathlib.Path(target_dir).rglob(target_file_pattern))
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
