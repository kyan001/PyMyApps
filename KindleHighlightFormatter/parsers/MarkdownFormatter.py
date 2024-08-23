class MarkdownFormatter:
    @classmethod
    def to_text(cls, info: dict = {}, export_h3: bool = True, export_color: bool = False, export_page: bool = False):
        markdowns = []
        title = info[".bookTitle"].lstrip("《").rstrip("》") if info.get(".bookTitle") else ""
        markdowns.append(f"# § 《{title}》{info.get('.authors')}")
        h3_cache = ""
        for highlight in info.get('highlights') or []:
            for selector, value in highlight.items():
                if selector == ".sectionHeading":
                    markdowns.append(f"## {value}")
                elif selector == ".noteHeading":
                    if export_h3 and (heading := value.get("heading")):
                        if heading != h3_cache:  # if h3 is not the previous one
                            h3_cache = heading
                            markdowns.append(f"### {heading}")
                    if export_color and (color := value.get("color")):
                        markdowns.append(color)
                    if export_page and (page := value.get("page")):
                        markdowns.append(page)
                elif selector == ".noteText":
                    markdowns.append(f"> {value}")
        return "\n\n".join(markdowns)
