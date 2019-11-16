import tempfile
import shutil
import os
import difflib

from KyanToolKit import KyanToolKit as ktk
import consoleiotools as cit


def diff(from_path: str, to_path: str):
    with open(from_path, encoding='utf-8') as f:
        from_lines = f.readlines()
    with open(to_path, encoding='utf-8') as f:
        to_lines = f.readlines()
    return list(difflib.unified_diff(from_lines, to_lines))


def final_strategy_replace(filename="shdwrckt_gfwlst.conf"):
    with tempfile.TemporaryDirectory() as tmp_filedir:
        filedirpath, filedirname = ktk.getDir(filename)
        tmp_filepath = os.path.join(tmp_filedir, filename)
        filepath = os.path.join(filedirpath, filename)
        with open(filepath, "rt", encoding='utf-8') as old_file, open(tmp_filepath, "wt", encoding='utf-8') as tmp_file:
            tmp_file.write(old_file.read().replace("FINAL,PROXY", "FINAL,DIRECT"))
        diffs = diff(filepath, tmp_filepath)
        if diffs:
            cit.warn("Diffs found:\n" + "".join(diffs))
            cit.ask("Does this look good?")
            if cit.get_choice(["Yes", "No"]) == "Yes":
                os.remove(filepath)
                shutil.move(tmp_filepath, filepath)
                cit.info("File replacement done.")
            else:
                cit.info("File not replaced.")
        else:
            cit.info("No need to replace the final strategy")


def main():
    ktk.updateFile("./shdwrckt_gfwlst.conf", "https://raw.githubusercontent.com/XinSSS/Conf-for-Surge-Shadowrocket/master/configFileHere/shadowrocket_gfwlist%26whiteIP.conf")
    final_strategy_replace()


if __name__ == "__main__":
    main()
