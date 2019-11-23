# -*- coding: utf-8 -*-
import sys
import os
import re
import tkinter
import tkinter.filedialog
import argparse

import consoleiotools as cit


__version__ = '1.2.1'
__prog__ = "AutoRename"
__description__ = "Auto rename files in a folder"
__epilog__ = "TL;DR: Run program with no args, or drag & drop a folder on it."

# Global Variables
PATTERN = r'S[0-9][0-9]E[0-9][0-9]'
DIVIDER = '-'


@cit.as_session
def get_file_dir(filedir=os.getcwd()):
    """Get file dir path

    Args:
        filedir: str.

    Returns:
        filedir: string of files' dir
    """
    cit.ask('Set file dir to "{}"?'.format(filedir))
    how_to_locate = cit.get_choice(['Yes', 'No, let me select', 'No, let me type'])
    if how_to_locate == 'No, let me select':  # manually select
        tkapp = tkinter.Tk()
        filedir = tkinter.filedialog.askdirectory()
        tkapp.destroy()
    elif how_to_locate == 'No, let me type':  # manually type
        filedir = cit.get_input('Please enter your dir:').strip('"').strip("'")
    cit.info('File dir: "{}"'.format(filedir))
    return filedir


@cit.as_session
def get_files(filedir: str):
    """Get all the file names in the path

    Args:
        filedir: the folder path of the files' dir

    Returns:
        files: list of files in filedir
    """
    if os.path.isdir(filedir):
        files = os.listdir(filedir)
    else:
        cit.err('"{}" is not a path'.format(filedir)).bye()
    cit.info('File list:')
    for fname in files:
        cit.echo(fname)
    return files


@cit.as_session
def get_keyword(filedir: str):
    """Get Keyword as the 1st part of the new filename

    Args:
        filedir: str

    Returns:
        keyword: str
    """
    global DIVIDER
    if os.path.isdir(filedir):
        keyword = os.path.split(filedir)[-1].replace(' ', '_')
    else:
        cit.err("'{}' is not a path".format(filedir)).bye()
    cit.ask("Set keyword to '{}' and divider to '{}'?".format(keyword, DIVIDER))
    if cit.get_choice(["Yes", "No"]) == "No":
        keyword = cit.get_input("Please enter new keyword:")
        DIVIDER = cit.get_input("Please enter new divider:")
    cit.info("Keyword: '{}'".format(keyword))
    return keyword


@cit.as_session('Get Name Mapping')
def get_name_map(files: list, keyword: str):
    """Get name mapping, old name as key, new name as value

    Args:
        files: list
        keyword: str

    Returns:
        namemap: dict

    Globals:
        PATTERN: pattern to test
        DIVIDER: divider between keyword and pattern matches
    """
    def set_new_pattern(pattern=None):
        global PATTERN
        PATTERN = pattern or cit.get_input("Please enter a new pattern: `[0-9][a-Z].+*()`")
        return get_name_map(files, keyword)

    # validations
    global PATTERN
    global DIVIDER
    if not files:
        cit.err('No file list')
        cit.bye()
    if not PATTERN:
        cit.err('No pattern detected.')
    cit.info('Testing pattern: `{}`'.format(PATTERN))
    # generate namemap
    namemap = {}
    for filename in files:
        froot, fext = os.path.splitext(filename)
        mtch = re.compile(PATTERN).findall(froot)
        if not mtch:
            cit.warn('Ignored: {}'.format(filename))
        else:
            cit.info('Matched: "{n}" : "{m}"'.format(n=filename, m=mtch[0]))
            to_name = "{kw}{div}{num}{ext}".format(kw=keyword, div=DIVIDER, num=mtch[0], ext=fext)
            namemap[filename] = to_name
    # check if namemap and pattern is ok
    if namemap:
        cit.ask("Set number's pattern to '{}'?".format(PATTERN))
        if cit.get_choice(['Yes', 'No']) == 'Yes':
            cit.info('Pattern: "{}"'.format(PATTERN))
            return namemap
    else:
        cit.warn('Pattern does not match any file!')
    PATTERN = cit.get_input("Please enter a new pattern: `[0-9] [a-Z] . * + ()`")
    return get_name_map(files, keyword)


def generate_cmds(filedir: str, namemap: dict):
    """Generate commands for rename

    Args:
        filedir: str
        namemap: dict

    Returns:
        A list contains all the commands
    """
    cmdlist = []
    os_rename_cmd = "rename" if "win32" in sys.platform else "mv"
    for (filename, to_name) in namemap.items():
        fullpath = os.path.join(filedir, filename)
        cmmnd = 'rename "{fp}" "{t}"'.format(fp=fullpath, t=to_name)
        cmdlist.append(cmmnd)
    return cmdlist


if __name__ == '__main__':
    # Args
    parser = argparse.ArgumentParser(prog=__prog__, description=__description__, epilog=__epilog__)
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument(dest="filedir", metavar="FILEDIR", nargs="?", default=os.getcwd(), help="Folder path of target files.")
    parser.add_argument("-k", "--keyword", dest="keyword", help="Prefix of new filename.")
    parser.add_argument("-p", "--pattern", dest="pattern", default=PATTERN, help="REGEX (REGular EXpression) which matches a part of filenames.")
    parser.add_argument("-d", "--divider", dest="divider", default=DIVIDER, help="Divider between keyword and matches.")
    parser.add_argument("-f", "--file", dest="files", action="append", nargs="*", help="target files in filedir, repeat it to add more files.")
    args = parser.parse_args()
    # get Vars
    PATTERN = args.pattern
    DIVIDER = args.divider
    filedir = get_file_dir(args.filedir)
    files = args.files or get_files(filedir)
    keyword = args.keyword or get_keyword(filedir)
    namemap = get_name_map(files=files, keyword=keyword)
    # get cmd
    cmds = generate_cmds(filedir=filedir, namemap=namemap)
    cit.warn('Commands example for final comfirm:')
    cit.echo(cmds[0])
    cit.pause('Press enter to run {} commands (Ctrl+C to Quit)...'.format(len(cmds)))
    # execute
    for c in cmds:
        os.system(c)
    cit.pause('[ Done ] ({} files)'.format(len(cmds)))
