import time
import enum
import json
import os
from collections import Counter

import tqdm
import consoleiotools as cit
import consolecmdtools as cct

import keyboardsimulator as kbs


SCORE_THRESHOLD = 24
ENABLED = {
    "WEBHOOK": False,
    "STATISTICS": False,
    "SCORE_THRESHOLD": False,
    "IQ_100": False,
    "SWORD_HIGH": True,
}


class Rarity(enum.Enum):
    GRAY = (93, 93, 93)
    GREEN = (88, 127, 82)
    BLUE = (74, 91, 163)
    PURPLE = (126, 59, 153)
    ORANGE = (235, 128, 67)
    RED = (153, 49, 49)


RARITY_WEIGHT = {
    "GRAY": 0,
    "GREEN": 0,
    "BLUE": 0,
    "PURPLE": 5,
    "ORANGE": 8,
    "RED": 10,
}

CHECKPOINT = {
    "IQ_HIGH": (526, 1070),
    "IQ_100": (652, 1067),
    "REROLL": (1084, 320),
    "BUFFS_X": [1625, 1875, 2129],
    "BUFFS_Y": [577, 671],
    "SWORD_HIGH": (1333, 1007)
}
CHECKCOLOR = {
    "IQ_HIGH_KO": (206, 207, 209),
    "IQ_100_OK": (50, 50, 50),
    "SWORD_HIGH_KO": (233, 232, 230),
}

WEBHOOK_FILE = os.path.join(cct.get_dir(__file__), "GGBH-WEBHOOK.txt")
WEBHOOK_URL = None
if os.path.isfile(WEBHOOK_FILE) and ENABLED["WEBHOOK"]:
    with open(WEBHOOK_FILE) as fl:
        WEBHOOK_URL = fl.read()


class RarityCounter(Counter):
    def __init__(self, color_counter: Counter):
        super().__init__()
        self.origin = color_counter
        for r in Rarity:
            self[r.name] = color_counter[r.value]
        self.validate()

    def validate(self):
        if sum(self.values()) != len(CHECKPOINT["BUFFS_X"]) * len(CHECKPOINT["BUFFS_Y"]):
            cit.err(f"Counter Error: Not all counter counts.")
            cit.err(f"Oringal Counter: {self.origin}")
            cit.err(f"Rarity Counter: {self}")
            cit.bye()

    def __str__(self) -> str:
        return json.dumps(self)

    def score(self, weights) -> int:
        return sum([weights[rw] * self[rw] for rw in weights])


class StatisticsCounter(Counter):
    def __init__(self, rarities: enum.Enum):
        super().__init__()
        self.Rarity = rarities
        self["IQ_HIGH"] = 0

    def print_rarity_statistics(self):
        total = sum([self[r.name] for r in self.Rarity])
        if total:
            cit.info("Rarity Statistics:")
            for r in self.Rarity:
                cit.echo(f"{r.name.ljust(9)}: {self[r.name] / total:.0%} ({self[r.name]}/{total})")

    def print_iq_statistics(self, total):
        if total:
            cit.info(f"IQ Statistics: {self['IQ_HIGH']/total:.0%} high. ({self['IQ_HIGH']}/{total})")

    def __str__(self):
        return json.dumps(self)


def grab_rarities() -> Counter:
    time.sleep(0.75)
    color_cntr = Counter([kbs.grab_color((x, y)) for y in CHECKPOINT["BUFFS_Y"] for x in CHECKPOINT["BUFFS_X"]])
    rarity_cntr = RarityCounter(color_cntr)
    return rarity_cntr


def notify(*texts, webhook: str = None):
    for text in texts:
        cit.warn(text)
    if ENABLED["WEBHOOK"] and WEBHOOK_URL:
        cct.ajax(webhook, {"text": "; ".join(texts)}, method="post")
    cit.pause()
    kbs.count_down(3)


def main():
    kbs.count_down(3)
    stat_cntr = StatisticsCounter(Rarity)
    loops = 0
    while True:
        flags = {}
        stat_cntr.print_iq_statistics(loops)
        stat_cntr.print_rarity_statistics()
        pbar = tqdm.tqdm(range(100), unit="roll")
        for i in pbar:
            loops += 1
            pbar.set_postfix(flags)
            pbar.set_description(f"Loop={loops}, IQ+={stat_cntr['IQ_HIGH']}")
            kbs.left_mouse_button(CHECKPOINT["REROLL"])
            time.sleep(1.25)
            flags["IQ_HIGH"] = kbs.grab_color(CHECKPOINT["IQ_HIGH"]) != CHECKCOLOR["IQ_HIGH_KO"]
            if ENABLED["IQ_100"]:
                flags["IQ_100"] = kbs.grab_color(CHECKPOINT["IQ_100"]) == CHECKCOLOR["IQ_100_OK"]
            if ENABLED["SWORD_HIGH"]:
                time.sleep(0.25)
                flags["SWORD_HIGH"] = kbs.grab_color(CHECKPOINT["SWORD_HIGH"]) != CHECKCOLOR["SWORD_HIGH_KO"]
            if not flags["IQ_HIGH"] and not ENABLED["STATISTICS"]:
                continue
            else:
                rarity_cntr = grab_rarities()
                score = rarity_cntr.score(RARITY_WEIGHT)
                if ENABLED["STATISTICS"]:
                    stat_cntr += rarity_cntr
                if flags["IQ_HIGH"]:
                    # cit.warn("High IQ detected!")
                    stat_cntr["IQ_HIGH"] += 1
                    if flags.get("IQ_100"):
                        notify("IQ100!")
                        continue
                    if flags.get("SWORD_HIGH"):
                        notify("Sword High!")
                        continue
                    if ENABLED["SCORE_THRESHOLD"] and score >= SCORE_THRESHOLD:
                        notify("Qualified BUFFs detected!")
                        continue


if __name__ == "__main__":
    main()
