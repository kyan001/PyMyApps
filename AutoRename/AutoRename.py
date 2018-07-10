# -*- coding: utf-8 -*-
import sys
import os
import re
import tkinter
import tkinter.filedialog
import argparse

import consoleiotools as cit


__version__ = '1.1.2'
__prog__ = "AutoRename"
__description__ = "Auto rename files in a folder"
__epilog__ = "TL;DR: Run program with no args, or drag & drop a folder on it."

# Global Variables
_PATTERN = r'S[0-9][0-9]E[0-9][0-9]'


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
    if os.path.isdir(filedir):
        keyword = os.path.split(filedir)[-1].replace(' ', '_')
    else:
        cit.err("'{}' is not a path".format(filedir)).bye()
    cit.ask("Set keyword to '{}'?".format(keyword))
    if cit.get_choice(["Yes", "No"]) == "No":
        keyword = cit.get_input("Please enter new keyword:")
    cit.info("Keyword: '{}'".format(keyword))
    return keyword


@cit.as_session('Get Name Mapping')
def get_name_map(pattern: str, files: list, keyword: str):
    """Get name mapping, old name as key, new name as value

    Args:
        pattern: pattern to test
        files: list
        keyword: str

    Returns:
        namemap: dict
    """
    # validations
    if not files:
        cit.err('No file list').bye()
    if not pattern:
        cit.warn('No pattern detected, use default pattern.')
        pattern = _PATTERN
    cit.info('Testing pattern: `{}`'.format(pattern))
    # generate namemap
    namemap = {}
    for fname in files:
        mtch = re.compile(pattern).findall(fname)
        if not mtch:
            cit.warn('Ignored: {}'.format(fname))
        else:
            cit.info('Matched: "{n}" : "{m}"'.format(n=fname, m=mtch[0]))
            fext = os.path.splitext(fname)[-1]
            to_name = "{kw}_{num}{ext}".format(kw=keyword, num=mtch[0], ext=fext)
            namemap[fname] = to_name
    # check if namemap and pattern is ok
    if namemap:
        cit.ask("Set number's pattern to '{}'?".format(pattern))
        if cit.get_choice(['Yes', 'No']) == 'Yes':
            cit.info('Pattern: "{}"'.format(pattern))
            return namemap
    else:
        cit.warn('Pattern does not match any file!')
    new_pattern = cit.get_input("Please enter a new pattern: `[0-9] [a-Z] . * + ()`")
    return get_name_map(new_pattern, files, keyword)


def generate_cmds(filedir: str, namemap: dict):
    """Generate commands for rename

    Args:
        filedir: str
        namemap: dict

    Returns:
        A list contains all the commands
    """
    cmdlist = []
    for (fname, to_name) in namemap.items():
        fullpath = "{d}/{n}".format(d=filedir, n=fname).replace('/', os.sep)
        cmmnd = 'rename "{fp}" "{t}"'.format(fp=fullpath, t=to_name)
        cmdlist.append(cmmnd)
    return cmdlist


if __name__ == '__main__':
    # Args
    parser = argparse.ArgumentParser(prog=__prog__, description=__description__, epilog=__epilog__)
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument(dest="filedir", metavar="FILEDIR", nargs="?", default=os.getcwd(), help="Folder path of target files.")
    parser.add_argument("-k", "--keyword", dest="keyword", help="Prefix of new filename.")
    parser.add_argument("-p", "--pattern", dest="pattern", default=_PATTERN, help="REGEX (REGular EXpression) which matches a part of filenames.")
    parser.add_argument("-f", "--file", dest="files", action="append", nargs="*", help="target files in filedir, repeat it to add more files.")
    args = parser.parse_args()
    # get Vars
    filedir = get_file_dir(args.filedir)
    files = args.files or get_files(filedir)
    keyword = args.keyword or get_keyword(filedir)
    namemap = get_name_map(pattern=args.pattern, files=files, keyword=keyword)
    # get cmd
    cmds = generate_cmds(filedir=filedir, namemap=namemap)
    cit.warn('Commands example for final comfirm:')
    cit.echo(cmds[0])
    cit.pause('Press enter to run {} commands (Ctrl+C to Quit)...'.format(len(cmds)))
    # execute
    for c in cmds:
        os.system(c)
    cit.pause('[ Done ] ({} files)'.format(len(cmds)))
