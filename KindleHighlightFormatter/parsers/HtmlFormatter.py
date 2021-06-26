import re

from bs4 import BeautifulSoup


class HtmlFormatter:
    @classmethod
    def parse(cls, html_file=""):
        info = {
            "title": "",
            "highlights": [],
        }
        soup = BeautifulSoup(open(html_file, encoding="utf8"), "lxml")
        title_div = soup.select_one(".bookTitle")
        info["title"] = title_div.get_text(strip=True) if title_div else ""
        authors_div = soup.select_one(".authors")
        info["authors"] = authors_div.get_text(strip=True) if title_div else ""
        for tag in soup.find_all("div", {"class": ["sectionHeading", "noteText", "noteHeading"]}):
            if "sectionHeading" in tag["class"]:
                highlight = {
                    "type": "sectionHeading",
                    "content": tag.get_text(strip=True),
                }
            if "noteHeading" in tag["class"]:
                highlight = {
                    "type": "noteHeading",
                }
                tag_text = tag.get_text(strip=True)
                matches = re.compile("(.*) - (.*) > (.*)").search(tag_text)
                if matches:
                    highlight["heading"] = matches.group(2)
                    highlight["page"] = matches.group(3)
                else:
                    highlight["page"] = tag_text.split(" - ")[-1]
                if tag.span and tag.span["class"][0].startswith("highlight_"):
                    highlight["color"] = tag.span.get_text(strip=True)
            if "noteText" in tag["class"]:
                highlight = {
                    "type": "noteText",
                    "content": tag.get_text(strip=True),
                }
            info["highlights"].append(highlight)
        return info
