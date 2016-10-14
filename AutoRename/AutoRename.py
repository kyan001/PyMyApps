# -*- coding: utf-8 -*-
import os
import re
import tkinter
import tkinter.filedialog
import consoleiotools as cit


class G(object):
    """Global Variables"""
    filedir = ''
    filelist = []
    keyword = ''
    pattern = ''
    namemap = {}


@cit.as_session('-- Get file dir --')
def getFiledir():
    """Get file dir path

    Set:
        G.filedir (str)
    """
    filedir = os.getcwd()
    cit.ask('Set file dir to "{}"?'.format(filedir))
    how_to_locate = cit.get_choice(['Yes', 'No, let me select', 'No, let me type'])
    if how_to_locate == 'No, let me select':
        tkapp = tkinter.Tk()
        filedir = tkinter.filedialog.askdirectory()
        tkapp.destroy()
    elif how_to_locate == 'No, let me type':
        filedir = cit.get_input('Please enter your dir:').strip('"').strip("'")
    cit.info('File dir: "{}"'.format(filedir))
    G.filedir = filedir
    return


@cit.as_session('-- Get file list --')
def getFilelist():
    """Get all the file names in the path

    Read:
        G.filedir: str
    Set:
        G.filelist: list
    """
    if os.path.isdir(G.filedir):
        filelist = os.listdir(G.filedir)
    else:
        cit.err('"{}" is not a path'.format(G.filedir)).bye()
    cit.info('File list:')
    for fname in filelist:
        cit.echo(fname, lvl=1)
    G.filelist = filelist
    return


@cit.as_session('-- Get keyword --')
def getKeyword():
    """Get Keyword as the 1st part of the new filename

    Read:
        G.filedir: str
    Set:
        G.keyword: str
    """
    if os.path.isdir(G.filedir):
        keyword = os.path.split(G.filedir)[-1].replace(' ', '_')
    else:
        cit.err('"{}" is not a path'.format(G.filedir)).bye()
    cit.ask('Set keyword to "{}"?'.format(keyword))
    if cit.get_choice(['Yes', 'No']) == 'No':
        keyword = cit.get_input('Please enter new keyword:')
    cit.info('Keyword: "{}"'.format(keyword))
    G.keyword = keyword
    return


@cit.as_session('-- Get name mapping --')
def getNamemap(pttrn: str):
    """Get name mapping, old name as key, new name as value

    Args:
        pttrn: pattern to test
    Read:
        G.filelist: list
    Set:
        G.namemap: dict
    """
    namemap = {}
    for fname in G.filelist:
        mtch = re.compile(pttrn).findall(fname)
        if not mtch:
            cit.warn('Ignored: {}'.format(fname), lvl=2)
        else:
            cit.info('Matched: "{n}" : "{m}"'.format(n=fname, m=mtch[0]), lvl=2)
            fext = os.path.splitext(fname)[-1]
            to_name = "{kw}_{num}{ext}".format(kw=G.keyword, num=mtch[0], ext=fext)
            namemap[fname] = to_name
    G.namemap = namemap
    return


@cit.as_session('-- Get pattern --')
def getPattern(pttrn: str):
    """Get pattern for match the episode's number in filename

    Args:
        pttrn: input pattern for testing
    Read:
        G.filelist: list
    Set:
        G.pattern: str
    """
    cit.info('Testing pattern: {}'.format(pttrn), lvl=1)
    if not G.filelist:
        cit.err('No file list', lvl=1).bye()
    if not pttrn:
        cit.err('No pattern', lvl=1).bye()
    getNamemap(pttrn)
    if G.namemap:
        cit.ask('Set number pattern to "{}"?'.format(pttrn))
    else:
        cit.warn('No filename matched the pattern')
    if not G.namemap or cit.get_choice(['Yes', 'No']) == 'No':
        new_pttrn = cit.get_input('Please enter a new pattern')
        return getPattern(new_pttrn)
    cit.info('Pattern: "{}"'.format(pttrn))
    G.pattern = pttrn
    return


def generateCmds():
    """Generate commands for rename

    Read:
        G.filedir: str
        G.namemap: dict
    Returns:
        A list contains all the commands
    """
    cmdlist = []
    for (fname, to_name) in G.namemap.items():
        fullpath = "{d}/{n}".format(d=G.filedir, n=fname).replace('/', os.sep)
        cmmnd = 'rename "{fp}" "{t}"'.format(fp=fullpath, t=to_name)
        cmdlist.append(cmmnd)
    return cmdlist

if __name__ == '__main__':
    # get Vars
    getFiledir()
    getFilelist()
    getKeyword()
    getPattern(r'S[0-9][0-9]E[0-9][0-9]')
    # get cmd
    cmds = generateCmds()
    cit.warn('Commands example for final comfirm:')
    cit.echo(cmds[0], lvl=1)
    cit.pause('Press enter to run {} commands (Ctrl+C to Quit)...'.format(len(cmds)))
    # execute
    for c in cmds:
        os.system(c)
    cit.pause('[ Done ]')
