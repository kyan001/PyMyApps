import sys
import webbrowser

import consoleiotools as cit
from bs4 import BeautifulSoup
import requests
try:
    import pyperclip
    clipboard = pyperclip.paste()
    IS_CLIPBOARD = clipboard and clipboard.startswith("https://apps.apple.com/")
except ImportError:
    IS_CLIPBOARD = False


def get_url():
    if len(sys.argv) > 1:
        return sys.argv[1]
    if IS_CLIPBOARD:
        cit.info("Loaded URL from clipboard.")
        return clipboard
    return cit.get_input("Enter an App Store Detail URL:")


def get_url_html(url: str) -> str:
    if not url:
        cit.err("URL is required.")
        cit.bye()
    resp = requests.get(url)
    return resp.text


def get_icon_srcset(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    picture_tag = soup.select_one("body > div.ember-view > main section.section--hero.product-hero picture")
    if not picture_tag:
        cit.err("Tag <picture> not found.")
        cit.bye()
    png_tag = picture_tag.find("source", attrs={"type": "image/png"})
    if not png_tag:
        cit.err("Tag <source type='image/png'> not found.")
        cit.bye()
    srcset = png_tag["srcset"]
    return srcset


def get_icon_url(srcset: str) -> str:
    srcs = srcset.split(", ")
    widest = sorted([src.split() for src in srcs])[-1]
    return widest[0]


@cit.as_session("Extraction")
def extraction_result(icon_url: str):
    if not icon_url:
        cit.err("No icon url found.")
        cit.bye()
    else:
        cit.info("Icon URL:")
        cit.br()
        print(icon_url)
        cit.br()
        if not IS_CLIPBOARD:
            cit.get_input("Open in Browser?", "> Yes")
        webbrowser.open_new_tab(icon_url)


def main():
    url = get_url()
    html = get_url_html(url)
    srcset = get_icon_srcset(html)
    icon_url = get_icon_url(srcset)
    extraction_result(icon_url)


if __name__ == "__main__":
    main()
    if not IS_CLIPBOARD:
        cit.pause()
