#! .venv/bin/python
import consoleiotools as cit

from classes import RuleSet

RULES_FILE = "MyRules.toml"
CLASH_RULESET_FILENAME = "Clash-Rules-MyRules.yaml"
SHADOWROCKET_MODULE_FILENAME = "Shadowrocket-Module-MyRules.sgmodule"


def main():
    rules = RuleSet.RuleSet()
    cit.info("Parse Rules File")
    rules.from_toml(RULES_FILE)
    cit.info("Generate Clash Yaml File")
    clash_ruleset = rules.to_clash_ruleset()
    rules.save_to_file(clash_ruleset, CLASH_RULESET_FILENAME)
    cit.info("Generate ShadowRocket sgmodule File")
    shadowrocket_module = rules.to_shadowrocket_module()
    rules.save_to_file(shadowrocket_module, SHADOWROCKET_MODULE_FILENAME)


if __name__ == "__main__":
    main()
    cit.pause()
