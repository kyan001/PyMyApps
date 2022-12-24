import sys
import webbrowser

import consoleiotools as cit
import bs4
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
    if resp.status_code == 200:
        cit.info(f"HTML loaded {resp.reason}. Content Length: {resp.headers['Content-Length']}.")
    else:
        cit.err(f"HTML loaded FAILED. Reason: {resp.status_code} {resp.reason}.")
        cit.bye()
    return resp.text


def get_tag(self, selector):
    tag = self.select_one(selector)
    mark = "[green]✓[/]" if tag else "[red]✕[/]"
    cit.info(f"{mark} [dim]<[/]{selector}[dim]>[/]")
    return tag


def get_icon_srcset(html: str) -> str:
    def get_image_tag(root_tag):
        for mime in ("image/png", "image/jpg", "image/webp"):
            image_tag = root_tag.find("source", attrs={"type": mime})
            if image_tag:
                return image_tag
        return None

    bs4.BeautifulSoup.get_tag = get_tag
    bs4.element.Tag.get_tag = get_tag
    soup = bs4.BeautifulSoup(html, "html.parser")
    picture_tag = soup.get_tag("body > div.ember-view").get_tag("main").get_tag("section.section--hero.product-hero").get_tag("picture")
    # picture_tag = soup.select_one("body > div.ember-view > main section.section--hero.product-hero picture")
    if not picture_tag:
        cit.err("Tag <picture> not found.")
        cit.bye()
    image_tag = get_image_tag(picture_tag)
    if not image_tag:
        cit.err("Tag <source type='image/[png|jpg|webp]'> not found.")
        cit.bye()
    srcset = image_tag["srcset"]
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
            if cit.get_input("Open in Browser? [cyan](yes)[/]", prompt="> [dim]yes[/] ") == "":
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
