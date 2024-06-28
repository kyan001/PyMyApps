#! .venv/bin/python
import argparse
import tkinter
import tkinter.filedialog
import sys

from bs4 import BeautifulSoup

import consoleiotools as cit
import consolecmdtools as cct

from parsers.HtmlFormatter import HtmlFormatter
from parsers.MarkdownFormatter import MarkdownFormatter


__version__ = '1.2.1'
__prog__ = "Kindle Highlight Formatter"
__description__ = "Convert Kindle Highlight HTML file into Markdown text"
__epilog__ = "TL;DR: Run program with no args, or drag & drop a .html on it."


def get_file():
    cit.ask("Target File")
    if cit.get_choice(["Select", "Enter manually"]) == "Enter manually":
        return cit.get_input("Please enter your file path:")
    else:
        return cct.select_path(filetypes=[("HTML file", ".html")])


def generate_markdown(html_file):
    info = HtmlFormatter.parse(html_file)
    markdown_text = MarkdownFormatter.to_text(info)
    return markdown_text


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__prog__, description=__description__, epilog=__epilog__)
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument(dest="file", metavar="FILE", nargs="?", default=sys.argv[1] if len(sys.argv) > 1 else None, help="target .html file.")
    args = parser.parse_args()
    # get markdown text
    html_file = args.file or get_file()
    markdown_text = generate_markdown(html_file)
    # how to deal
    cit.ask("How to deal with the markdown text?")
    if cit.get_choice(['Show', 'Copy to clipboard']) == 'Show':
        cit.echo(markdown_text)
    else:
        import pyperclip
        pyperclip.copy(markdown_text)
        cit.info("Copy success.")
    cit.pause()
