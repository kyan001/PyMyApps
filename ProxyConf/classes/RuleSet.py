import os
import tempfile
import tomllib

import consoleiotools as cit
import consolecmdtools as cct


class RuleSet:
    def __init__(self) -> None:
        self.rules: list[dict] = []

    def from_toml(self, filename: str):
        if not filename:
            raise ValueError("filename is required")
        path = cct.get_path(filename)
        if not path.exists:
            raise FileNotFoundError(f"file not found: {path}")
        with open(path, "rb") as fl:
            toml_data = tomllib.load(fl)
        default = toml_data['default']
        count = 0
        for r in toml_data['rules']:
            rule = {**default, **r}  # kv in r overwrites kv in default
            if not rule.get('arg'):
                cit.warn(f"Skipped! Rule has no argument: {rule}")
                continue
            if rule['policy'] != "PROXY":
                cit.warn(f"Skipped! Rule policy is not `PROXY`: {rule}")
                continue
            count += 1
            self.rules.append(rule)
        cit.info(f"{count}/{len(toml_data['rules'])} rules loaded.")

    @staticmethod
    def rule_comment(rule) -> str:
        comment = ["#"]
        if rule['blocked']:
            comment.append("BLOCKED!")
        if rule['redirected']:
            comment.append("REDIRECTED!")
        if rule['desc']:
            comment.append(rule['desc'])
        if len(comment) == 1:
            return ""
        return " ".join(comment)

    def to_clash_ruleset(self) -> str:
        result = ["payload:"]
        for rule in self.rules:
            text = f"  - {rule['type']}, {rule['arg']}"
            comment = self.rule_comment(rule)
            if comment:
                text += "  " + comment
            result.append(text)
        return "\n".join(result)

    def to_shadowrocket_module(self) -> str:
        result = ["#!name=ShadowRocket My Rules", "#!desc=ShadowRocket My Rules", "", "[Rule]"]
        for rule in self.rules:
            text = f"{rule['type']}, {rule['arg']}, {rule['policy']}"
            comment = self.rule_comment(rule)
            if comment:
                text += "  " + comment
            result.append(text)
        return "\n".join(result)

    def save_to_file(self, content: str, filename: str):
        if not filename:
            cit.err("No filename specified.")
            return False
        if not content:
            cit.err("No content to save.")
            return False
        with tempfile.TemporaryDirectory() as tmp_filedir:
            tmp_filepath = os.path.join(tmp_filedir, filename)
            current_dir = cct.get_path(__file__).parent
            filepath = os.path.join(current_dir, filename)
            with open(tmp_filepath, "wt", encoding='utf-8') as tmp_file:
                tmp_file.write(content)
            cct.move_file(tmp_filepath, filepath)
            cit.info(f"File saved to {filepath}")
        return True
