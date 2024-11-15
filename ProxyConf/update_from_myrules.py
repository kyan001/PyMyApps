#! .venv/bin/python
import os

import consoleiotools as cit
import consolecmdtools as cct

from classes import RuleSet

RULES_FILE = "MyRules.toml"
CLASH_RULESET_FILENAME = "Clash-Rules-MyRules.yaml"
SHADOWROCKET_MODULE_FILENAME = "Shadowrocket-Module-MyRules.sgmodule"


def main():
    rules = RuleSet.RuleSet()
    current_dir = cct.get_path(__file__).parent
    cit.title("Parse Rules File")
    rules.from_toml(RULES_FILE)
    # Clash
    cit.title("Generate Clash Yaml File")
    clash_ruleset_path = os.path.join(current_dir, CLASH_RULESET_FILENAME)
    clash_ruleset = rules.to_clash_ruleset()
    rules.save_to_file(clash_ruleset, clash_ruleset_path)
    # ShadowRocket
    cit.title("Generate ShadowRocket sgmodule File")
    shadowrocket_module_path = os.path.join(current_dir, SHADOWROCKET_MODULE_FILENAME)
    shadowrocket_module = rules.to_shadowrocket_module()
    rules.save_to_file(shadowrocket_module, shadowrocket_module_path)


if __name__ == "__main__":
    main()
    cit.pause()
