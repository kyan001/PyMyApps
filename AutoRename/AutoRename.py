# -*- coding: utf-8 -*-
import sys
import os
import re
import tkinter
import tkinter.filedialog
import consoleiotools as cit


__version__ = '1.0.2'

# Global Variables
_PATTERN = r'S[0-9][0-9]E[0-9][0-9]'


@cit.as_session
def get_file_dir():
    """Get file dir path

    Returns:
        filedir: string of files' dir
    """
    if len(sys.argv) > 1:  # if drag & drop folder on .py file
        filedir = sys.argv[1]
    else:  # .py file is in the files' folder or manually set
        filedir = os.getcwd()
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
def get_file_list(filedir: str):
    """Get all the file names in the path

    Args:
        filedir: the folder path of the files' dir

    Returns:
        filelist: list of files in filedir
    """
    if os.path.isdir(filedir):
        filelist = os.listdir(filedir)
    else:
        cit.err('"{}" is not a path'.format(filedir)).bye()
    cit.info('File list:')
    for fname in filelist:
        cit.echo(fname)
    return filelist


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
def get_name_map(pattern: str, filelist: list, keyword: str):
    """Get name mapping, old name as key, new name as value

    Args:
        pattern: pattern to test
        filelist: list
        keyword: str

    Returns:
        namemap: dict
    """
    # validations
    if not filelist:
        cit.err('No file list').bye()
    if not pattern:
        cit.warn('No pattern detected, use default pattern.')
        pattern = _PATTERN
    cit.info('Testing pattern: `{}`'.format(pattern))
    # generate namemap
    namemap = {}
    for fname in filelist:
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
    return get_name_map(new_pattern, filelist, keyword)


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
    # get Vars
    filedir = get_file_dir()
    filelist = get_file_list(filedir)
    keyword = get_keyword(filedir)
    namemap = get_name_map(pattern=_PATTERN, filelist=filelist, keyword=keyword)
    # get cmd
    cmds = generate_cmds(filedir=filedir, namemap=namemap)
    cit.warn('Commands example for final comfirm:')
    cit.echo(cmds[0])
    cit.pause('Press enter to run {} commands (Ctrl+C to Quit)...'.format(len(cmds)))
    # execute
    for c in cmds:
        os.system(c)
    cit.pause('[ Done ] ({} files)'.format(len(cmds)))
