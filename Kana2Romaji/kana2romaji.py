import sys

import consoleiotools as cit

import jisho


__version__ = '1.0.0'


@cit.as_session
def romajify(kana: str) -> str:
    cit.info(f"{len(kana)} chars received.")
    romaji = kana
    KANAJISHOS = (
        jisho.katakana_youon,
        jisho.hiragana_youon,
        jisho.katakana,
        jisho.hiragana,
        jisho.sutegana,
    )
    for kanajisho in KANAJISHOS:
        for kn, rmj in kanajisho.items():
            romaji = romaji.replace(kn, f"{rmj} ")
    romaji = romaji.replace(" )", ")")  # remove redundant space before right quotes.
    romaji = romaji.replace(")", ") ")  # add space after right quotes.
    romaji = romaji.replace("　", ", ")  # replace japanese space with comma.
    cit.info(f"{len(romaji)} chars translated.")
    return romaji


@cit.as_session
def get_source_text():
    cit.ask("How can I get the source text?")
    choices = {
        "file": "Select a file",
        "filepath": "Enter a file path",
        "simpletext": "Type in single-line text",
        "multitext": "Type in multi-line text",
        "paste": "Paste from clipboard"
    }
    selection = cit.get_choice(list(sorted(choices.values())))
    if selection == choices['file']:
        import tkinter
        import tkinter.filedialog
        tkapp = tkinter.Tk()
        filepath = tkinter.filedialog.askopenfilename()
        tkapp.destroy()
        return cit.read_file(filepath)
    elif selection == choices['filepath']:
        filepath = cit.get_input('Filepath> ').strip('"').strip("'")
        return cit.read_file(filepath)
    elif selection == choices['simpletext']:
        return input("仮名> ")
    elif selection == choices['multitext']:
        eof_shortcut = "⌃Ctrl + Z" if "win32" in sys.platform else "⌃Ctrl + D"
        cit.ask(f"Please type of paste your text here: (Press `{eof_shortcut}` and `↩︎Enter` at the end of input)")
        multilines = sys.stdin.readlines()
        return "".join(multilines)
    elif selection == choices['paste']:
        import pyperclip
        return pyperclip.paste()


@cit.as_session
def save_text_to(romaji: str):
    length = len(romaji) / 1024
    length_text = "<1" if length < 1 else f'{length:.2f}'
    cit.info(f"Text size: {length_text} kB")
    while True:
        cit.ask("What do you want to do with the translated text? (Ctrl + C to exit)")
        choices = {
            "save": "Save as `romajified.txt`",
            "copy": "Copy to clipboard",
            "print": "Print on screen",
        }
        selection = cit.get_choice(list(sorted(choices.values())))
        if selection == choices['save']:
            import tkinter
            import tkinter.filedialog
            import os
            tkapp = tkinter.Tk()
            folderpath = tkinter.filedialog.askdirectory()
            filepath = os.path.join(folderpath, 'romajified.txt')
            tkapp.destroy()
            if not os.path.isdir(folderpath):
                cit.warn(f"Folder {folderpath} does not exist, created")
                os.makedirs(folderpath)
            if os.path.isfile(filepath):
                cit.err(f"file {filepath} is alread existed!")
                continue
            cit.write_file(path=filepath, content=romaji)
            cit.info(f"File saved at {filepath}")
        elif selection == choices['copy']:
            import pyperclip
            pyperclip.copy(romaji)
        elif selection == choices['print']:
            print(romaji)


if __name__ == '__main__':
    kana_text = get_source_text()
    romaji_text = romajify(kana_text)
    save_text_to(romaji_text)
