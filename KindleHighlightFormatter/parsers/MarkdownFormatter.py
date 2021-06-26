class MarkdownFormatter:
    @classmethod
    def to_text(cls, info: dict = None):
        markdowns = []
        if info.get("title") or info.get("authors"):
            markdowns.append(f"# § 《{info.get('title')}》{info.get('authors')}")
        for highlight in info.get('highlights'):
            if highlight["type"] == "sectionHeading":
                markdowns.append(f"## {highlight['content']}")
            elif highlight["type"] == "noteHeading":
                continue  # comment this line to add heading info
                if highlight.get("heading"):
                    markdowns.append(f"### {highlight['heading']}")
                if highlight.get("color"):
                    markdowns.append(f"{highlight['color']}")
                markdowns.append(f"{highlight['page']}")
            elif highlight["type"] == "noteText":
                markdowns.append(f"> {highlight['content']}")
        return "\n\n".join(markdowns)
