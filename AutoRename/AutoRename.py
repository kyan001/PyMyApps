# -*- coding: utf-8 -*-
import os
import re
import tkinter
import tkinter.filedialog
import KyanToolKit
ktk = KyanToolKit.KyanToolKit()


class G(object):
    """Global Variables"""
    filedir = ''
    filelist = []
    keyword = ''
    pattern = ''
    namemap = {}


def getFiledir():
    """Get file dir path

    Set:
        G.filedir (str)
    """
    ktk.pStart().pTitle('-- Get file dir --')
    filedir = os.getcwd()
    ktk.echo('Set file dir to "{}"?'.format(filedir))
    how_to_locate = ktk.getChoice(['Yes', 'No, let me select', 'No, let me type'])
    if how_to_locate == 'No, let me select':
        tkapp = tkinter.Tk()
        filedir = tkinter.filedialog.askdirectory()
        tkapp.destroy()
    elif how_to_locate == 'No, let me type':
        filedir = ktk.getInput('Please enter your dir:').strip('"').strip("'")
    ktk.info('File dir: "{}"'.format(filedir))
    ktk.pEnd()
    G.filedir = filedir
    return


def getFilelist():
    """Get all the file names in the path

    Read:
        G.filedir: str
    Set:
        G.filelist: list
    """
    ktk.pStart().pTitle('-- Get file list --')
    if os.path.isdir(G.filedir):
        filelist = os.listdir(G.filedir)
    else:
        ktk.err('"{}" is not a path'.format(G.filedir)).bye()
    ktk.info('File list:')
    for fname in filelist:
        ktk.echo(fname, lvl=1)
    ktk.pEnd()
    G.filelist = filelist
    return


def getKeyword():
    """Get Keyword as the 1st part of the new filename

    Read:
        G.filedir: str
    Set:
        G.keyword: str
    """
    ktk.pStart().pTitle('-- Get keyword --')
    if os.path.isdir(G.filedir):
        keyword = os.path.split(G.filedir)[-1].replace(' ', '_')
    else:
        ktk.err('"{}" is not a path'.format(G.filedir)).bye()
    ktk.echo('Set keyword to "{}"?'.format(keyword))
    if ktk.getChoice(['Yes', 'No']) == 'No':
        keyword = ktk.getInput('Please enter new keyword:')
    ktk.info('Keyword: "{}"'.format(keyword))
    ktk.pEnd()
    G.keyword = keyword
    return


def getNamemap(pttrn: str):
    """Get name mapping, old name as key, new name as value

    Args:
        pttrn: pattern to test
    Read:
        G.filelist: list
    Set:
        G.namemap: dict
    """
    ktk.pStart().pTitle('-- Get name mapping --')
    namemap = {}
    for fname in G.filelist:
        mtch = re.compile(pttrn).findall(fname)
        if not mtch:
            ktk.warn('Ignored: {}'.format(fname), lvl=2)
        else:
            ktk.info('Matched: "{n}" : "{m}"'.format(n=fname, m=mtch[0]), lvl=2)
            fext = os.path.splitext(fname)[-1]
            to_name = "{kw}_{num}{ext}".format(kw=G.keyword, num=mtch[0], ext=fext)
            namemap[fname] = to_name
    G.namemap = namemap
    return


def getPattern(pttrn: str):
    """Get pattern for match the episode's number in filename

    Args:
        pttrn: input pattern for testing
    Read:
        G.filelist: list
    Set:
        G.pattern: str
    """
    ktk.pStart().pTitle('-- Get pattern --')
    ktk.info('Testing pattern: {}'.format(pttrn), lvl=1)
    if not G.filelist:
        ktk.err('No file list', lvl=1).bye()
    if not pttrn:
        ktk.err('No pattern', lvl=1).bye()
    getNamemap(pttrn)
    if G.namemap:
        ktk.echo('Set number pattern to "{}"?'.format(pttrn))
    else:
        ktk.warn('No filename matched the pattern')
    if not G.namemap or ktk.getChoice(['Yes', 'No']) == 'No':
        new_pttrn = ktk.getInput('Please enter a new pattern')
        return getPattern(new_pttrn)
    ktk.info('Pattern: "{}"'.format(pttrn))
    ktk.pEnd()
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
    ktk.clearScreen()
    # get Vars
    getFiledir()
    getFilelist()
    getKeyword()
    getPattern(r'S[0-9][0-9]E[0-9][0-9]')
    # get cmd
    cmds = generateCmds()
    ktk.warn('Commands example for final comfirm:')
    ktk.echo(cmds[0], lvl=1)
    ktk.pressToContinue('Press enter to run {} commands (Ctrl+C to Quit)...'.format(len(cmds)))
    # execute
    for c in cmds:
        os.system(c)
    ktk.pressToContinue('[ Done ]')
