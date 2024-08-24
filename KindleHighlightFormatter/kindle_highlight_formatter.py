#! .venv/bin/python
import argparse
import sys

import consoleiotools as cit
import consolecmdtools as cct

from parsers.HtmlFormatter import HtmlFormatter
from parsers.MarkdownFormatter import MarkdownFormatter


__version__ = '1.2.3'
__prog__ = "Kindle Highlight Formatter"
__description__ = "Convert Kindle Highlight HTML file into Markdown text"
__epilog__ = "TL;DR: Run program with no args, or drag & drop a .html on it."


def copy_to_clipboard(text: str):
    if not text:
        return None  # copy failed
    try:
        import pyperclip
        pyperclip.copy(text)
        return True  # copy success
    except ModuleNotFoundError:
        return False  # no pyperclip module


def gui():
    from nicegui import ui  # lazy import
    data = {  # shared data
        "markdown": "",
    }

    def parse_highlights_html(event):
        html_text = event.content.read().decode("utf-8")
        info = HtmlFormatter.parse_html(html_text)
        data['markdown'] = MarkdownFormatter.to_text(info)

    def copy_markdown():
        markdown_text = data.get('markdown') or ""
        if copy_to_clipboard(markdown_text) is None:
            ui.notify("No markdown to copy.", type='negative')
        elif copy_to_clipboard(markdown_text) is False:
            ui.notify("Copy failed: Need 'pyperclip' module to copy.", type='negative')
        else:
            ui.notify("Copy success.", type='positive')

    with ui.row().classes("w-full"):
        ui.label(__prog__).classes("text-4xl w-full text-center")
        ui.label(__description__).classes("text-sm w-full text-center")
    with ui.dialog() as dialog, ui.card():
        ui.upload(label="Upload HTML file", auto_upload=True, on_upload=parse_highlights_html).props("accept=.html")
    ui.button("Upload exported HTML file for Kindle highlights", icon="upload_file", on_click=dialog.open).classes("w-full")
    with ui.card().classes("w-full").bind_visibility(data, 'markdown'):
        ui.markdown().bind_content_from(data, 'markdown').classes("w-full")
        with ui.button(icon='content_copy', on_click=copy_markdown).classes("absolute top-2 right-2"):
            ui.tooltip("Copy to clipboard")
    ui.run(
        title=__prog__,  # page title
        favicon="📑",  # page favicon
        dark=None,  # auto dark mode  # None: auto, True: dark, False: light
        reload=True,  # reload on change
    )


if __name__ in {'__main__', "__mp_main__"}:
    parser = argparse.ArgumentParser(prog=__prog__, description=__description__, epilog=__epilog__)
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument(dest="file", metavar="FILE", nargs="?", default=sys.argv[1] if len(sys.argv) > 1 else None, help="target .html file.")
    args = parser.parse_args()
    # get markdown text
    if args.file or cit.get_choice(['CLI mode', 'GUI mode'], default="GUI mode") == 'CLI mode':
        if not (filepath := args.file):
            cit.ask("Select exported HTML file for Kindle highlights")
            if cit.get_choice(["Select HTML file", "Manually Type Input"]) == "Manually Type Input":
                filepath = cit.get_input("Please enter your .html file path:")
            else:
                filepath = cct.select_path(filetypes=[("HTML file", ".html")])
        info = HtmlFormatter.parse_file(str(filepath))
        markdown_text = MarkdownFormatter.to_text(info)
        if copy_to_clipboard(markdown_text) is None:
            cit.err("No markdown to copy.")
        elif copy_to_clipboard(markdown_text) is False:
            cit.err("Copy failed: Need 'pyperclip' module to copy.")
        else:
            cit.info("Copy success.")
        if cit.get_input("Print markdown text? (Y/n)", default="n").lower() == "y":
            cit.echo(markdown_text)
        cit.pause()
    else:
        gui()
