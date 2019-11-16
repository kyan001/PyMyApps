import tempfile
import shutil
import os
import difflib


import KyanToolKit as ktk
import consoleiotools as cit


def diff(from_path: str, to_path: str):
    with open(from_path, encoding='utf-8') as f:
        from_lines = f.readlines()
    with open(to_path, encoding='utf-8') as f:
        to_lines = f.readlines()
    return list(difflib.unified_diff(from_lines, to_lines))


def replaceFinal(file_):
    old_filename = "shdwrckt_gfwlst.conf"
    new_filename = "new_shdwrck_gfwlst.conf"
    with open(old_filename, "rt") as old_file:
        with tempfile.TemporaryDirectory() as new_filedir:
            open(new_filename, "wt") as new_file:
                new_file.write(old_file.read().replace("FINAL,PROXY", "FINAL,DIRECT"))


def main():
    ktk.updateFile("./shdwrckt_gfwlst.conf", "https://raw.githubusercontent.com/XinSSS/Conf-for-Surge-Shadowrocket/master/configFileHere/shadowrocket_gfwlist%26whiteIP.conf")


if __name__ == "__main__":
    main()
