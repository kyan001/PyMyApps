import sys
import webbrowser

import consoleiotools as cit
import bs4
import requests
try:
    import pyperclip
except ImportError:
    cit.warn("Module `pyperclip` not found, clipboard is unavailable.")


def get_url():
    if len(sys.argv) > 1 and sys.argv[1].startswith("https://apps.apple.com/"):
        return sys.argv[1]
    if "pyperclip" in sys.modules:  # Check if the pyperclip module is imported
        clipboard = pyperclip.paste()
        if clipboard.startswith("https://apps.apple.com/"):
            cit.info("Loaded URL from clipboard.")
            return clipboard
    return cit.get_input("Enter an App Store Detail URL:")


def get_url_html(url: str) -> str:
    if not url:
        cit.err("URL is required.")
        cit.bye()
    resp = requests.get(url)
    if resp.status_code == 200:
        cit.info(f"HTML loaded {resp.reason}. Content Length: {resp.headers.get('Content-Length')}.")
    else:
        cit.err(f"HTML loaded FAILED. Reason: {resp.status_code} {resp.reason}.")
        cit.bye()
    return resp.text


class TagPointer:
    def __init__(self, tag: bs4.element.Tag):
        self.tag = tag

    def __getattr__(self, name: str):
        return getattr(self.tag, name)

    def get_tag(self, selector: str):
        self.tag = self.select_one(selector)
        if self.tag is None:
            cit.info(f"[red]✕[/] [dim]<[/]{selector}[dim]>[/]")
            cit.err(f"Tag <{selector}> not found.")
            cit.bye()
        cit.info(f"[green]✓[/] [dim]<[/]{selector}[dim]>[/]")
        return self

    def find_image_tag(self):
        for mime in ("image/png", "image/jpg", "image/webp"):
            image_tag = self.tag.find("source", attrs={"type": mime})  # type: ignore
            if image_tag:
                self.tag = image_tag
                return self
        cit.err("Tag <source type='image/[png|jpg|webp]'> not found.")
        cit.bye()


def get_icon_srcset(html: str) -> str:
    soup = TagPointer(bs4.BeautifulSoup(html, "html.parser"))
    image_tag = soup.get_tag("body > div.ember-view").get_tag("main").get_tag("section.section--hero.product-hero").get_tag("picture").find_image_tag()
    srcset = image_tag.get("srcset")  # type: ignore
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
        cit.info(icon_url)
        cit.br()
        if "pyperclip" in sys.modules:
            pyperclip.copy(icon_url)
            cit.info("Icon URL is copied!")
        if cit.get_input("Open in Browser?", default="yes") == "yes":
            webbrowser.open_new_tab(icon_url)


def main():
    url = get_url()
    html = get_url_html(url)
    srcset = get_icon_srcset(html)
    icon_url = get_icon_url(srcset)
    extraction_result(icon_url)


if __name__ == "__main__":
    main()
    cit.pause()
