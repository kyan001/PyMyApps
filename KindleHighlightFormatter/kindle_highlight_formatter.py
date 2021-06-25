import argparse
import tkinter
import tkinter.filedialog
import sys

from bs4 import BeautifulSoup

import consoleiotools as cit


__version__ = '1.1.1'
__prog__ = "Kindle Highlight HTML to Markdown"
__description__ = "Convert Kindle Highlight HTML file into Markdown text"
__epilog__ = "TL;DR: Run program with no args, or drag & drop a .html on it."


def get_file():
    cit.ask("Target File")
    if cit.get_choice(["Select", "Enter manually"]) == "Enter manually":
        return cit.get_input("Please enter your file path:")
    else:
        tkapp = tkinter.Tk()
        filepath = tkinter.filedialog.askopenfilename(filetypes=[("HTML file", ".html")])
        tkapp.destroy()
        return filepath


def generate_markdown(html_file):
    markdown = []
    soup = BeautifulSoup(open(html_file, encoding="utf8"), 'lxml')
    title_div = soup.find(attrs={'class': "bookTitle"})
    if title_div:
        title = title_div.get_text(strip=True)
        markdown.append(f"# § 《{title}》")
    for tag in soup.select(".sectionHeading, .noteText"):
        if "sectionHeading" in tag['class']:
            markdown.append(f"## {tag.get_text(strip=True)}")
        if "noteText" in tag['class']:
            markdown.append(f"> {tag.get_text(strip=True)}")
    return "\n\n".join(markdown)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__prog__, description=__description__, epilog=__epilog__)
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument(dest="file", metavar="FILE", nargs="?", default=sys.argv[1] if len(sys.argv) > 1 else None, help="target .html file.")
    args = parser.parse_args()
    # get markdown text
    html_file = args.file or get_file()
    md_text = generate_markdown(html_file)
    # how to deal
    cit.ask("How to deal with the markdown text?")
    if cit.get_choice(['Show', 'Copy to clipboard']) == 'Show':
        cit.echo(md_text)
    else:
        import pyperclip
        pyperclip.copy(md_text)
        cit.info("Copy success.")
    cit.pause()
