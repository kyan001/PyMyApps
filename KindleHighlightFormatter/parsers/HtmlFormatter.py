import re

from bs4 import BeautifulSoup


class HtmlFormatter:
    @classmethod
    def parse(cls, html_file=""):
        """parse highlight html file into object

        Args:
            html_file (str, optional): path to highlight html file. Defaults to "".

        Returns:
            dict: {  # parsed highlight object
                ".bookTitle": str,  # book title
                ".authors": str,  # book authors
            }
        """
        info = {
            ".bookTitle": "",
            ".authors": "",
            "highlights": [],  # [{selector: value}, ...]
        }
        soup = BeautifulSoup(open(html_file, encoding="utf8"), "lxml")
        for selector in (".bookTitle", ".authors"):
            div = soup.select_one(selector)
            if div:
                info[selector] = div.get_text(strip=True)
        for tag in soup.select(".sectionHeading, .noteText, .noteHeading"):
            css_class = tag["class"][0]
            if css_class == "noteHeading":
                value = {}
                tag_text = tag.get_text(strip=True)  # type(<span>...</span>) - heading > page
                hl_type, hl_location = tag_text.split(" - ")
                if matches := re.compile(r"(?P<heading>.+?) > (?P<page>.+)").match(hl_location):
                    value.update(matches.groupdict())
                else:
                    value["page"] = hl_location
                if matches := re.compile(r"(?P<type>.+?)\((?P<color>.+?)\)").match(hl_type):
                    value.update(matches.groupdict())
                highlight = {".noteHeading": value}
            else:
                highlight = {f'.{css_class}': tag.get_text(strip=True)}
            info["highlights"].append(highlight)
        return info
