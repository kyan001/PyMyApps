class MarkdownFormatter:
    @classmethod
    def to_text(cls, info: dict = {}, export_h3: bool = True, export_color: bool = False, export_page: bool = False):
        markdowns = []
        h1 = "# § "
        h3_cache = ""
        if info.get("title"):
            if not info["title"].startswith("《"):
                h1 += "《"
            h1 += info["title"]
            if not info["title"].endswith("》"):
                h1 += "》"
        if info.get("authors"):
            h1 += info["authors"]
        markdowns.append(h1)
        for highlight in info.get('highlights') or []:
            if highlight["type"] == "sectionHeading":
                markdowns.append(f"## {highlight['content']}")
            elif highlight["type"] == "noteHeading" and export_h3:
                if highlight.get("heading") and export_h3:
                    if highlight['heading'] != h3_cache:
                        h3_cache = highlight['heading']
                        markdowns.append(f"### {highlight['heading']}")
                if highlight.get("color") and export_color:
                    markdowns.append(f"{highlight['color']}")
                if export_page:
                    markdowns.append(f"{highlight['page']}")
            elif highlight["type"] == "noteText":
                markdowns.append(f"> {highlight['content']}")
        return "\n\n".join(markdowns)
