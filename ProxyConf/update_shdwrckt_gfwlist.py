import tempfile
import shutil
import os
import difflib

import consolecmdtools as cct
import consoleiotools as cit


def diff(from_path: str, to_path: str):
    with open(from_path, encoding='utf-8') as f:
        from_lines = f.readlines()
    with open(to_path, encoding='utf-8') as f:
        to_lines = f.readlines()
    return list(difflib.unified_diff(from_lines, to_lines, n=0))


def final_strategy_replace(filename="shdwrckt_gfwlst.conf"):
    with tempfile.TemporaryDirectory() as tmp_filedir:
        filedirpath = cct.get_dir(filename)
        tmp_filepath = os.path.join(tmp_filedir, filename)
        filepath = os.path.join(filedirpath, filename)
        with open(filepath, "rt", encoding='utf-8') as old_file, open(tmp_filepath, "wt", encoding='utf-8') as tmp_file:
            file_content = old_file.read()
            cit.info("Replacing `FINAL` to `FINAL,DIRECT`")
            file_content = file_content.replace("FINAL,PROXY", "FINAL,DIRECT")
            cit.info("Replacing `dns-server` to `223.5.5.5,8.8.8.8`")
            file_content = file_content.replace("dns-server = 119.29.29.29,223.5.5.5", "dns-server = 223.5.5.5,8.8.8.8")
            tmp_file.write(file_content)
        cct.diff(filepath, tmp_filepath)
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
    cct.update_file("./shdwrckt_gfwlst.conf", "https://raw.githubusercontent.com/XinSSS/Conf-for-Surge-Shadowrocket/master/configFileHere/shadowrocket_gfwlist%26whiteIP.conf")
    final_strategy_replace()


if __name__ == "__main__":
    main()
