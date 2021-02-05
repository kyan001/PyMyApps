import time
import enum
import json
from collections import Counter

import tqdm
import consoleiotools as cit
import consolecmdtools as cct

import keyboardsimulator as kbs


SCORE_QUALIFIED = 40
SCORE_EXTRAORDINARY = 50
RARITY_STATISTICS = False
# RARITY_STATISTICS = True


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
    "PURPLE": 1,
    "ORANGE": 8,
    "RED": 10,
}

REROLL_CLICK_POINT = (1084, 320)
IQ_BACKGROUND_COLOR = (206, 207, 209)
IQ_CHECK_POINT = (526, 1070)
BUFF_POINTS_X = [1625, 1875, 2129]
BUFF_POINTS_Y = [577, 671]
BUFF_POINTS_COUNT = len(BUFF_POINTS_X) * len(BUFF_POINTS_Y)
NOTIFY_WEBHOOK = "https://hooks.slack.com/services/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"


class RarityCounter(Counter):
    def __init__(self, color_counter: Counter):
        super().__init__()
        self.origin = color_counter
        for r in Rarity:
            self[r.name] = color_counter[r.value]
        self.validate()

    def validate(self):
        if sum(self.values()) != BUFF_POINTS_COUNT:
            cit.err(f"Counter Error: Not all counter counts.")
            cit.err(f"Oringal Counter: {self.origin}")
            cit.err(f"Rarity Counter: {self}")
            cit.bye()

    def __str__(self) -> str:
        return json.dumps(self)

    def score(self, weights) -> int:
        highest_weight = sorted(weights.values())[-1] * BUFF_POINTS_COUNT
        return sum([weights[rw] * self[rw] for rw in weights]) * 100 // highest_weight


class StatisticsCounter(Counter):
    def __init__(self, rarities: enum.Enum):
        super().__init__()
        self.Rarity = rarities
        self['HighIQ'] = 0

    def print_rarity_statistics(self):
        total = sum([self[r.name] for r in self.Rarity])
        if total:
            cit.info("Rarity Statistics:")
            for r in self.Rarity:
                cit.echo(f"{r.name.ljust(9)}: {self[r.name] / total:.0%} ({self[r.name]}/{total})")

    def print_iq_statistics(self, total):
        if total:
            cit.info(f"IQ Statistics: {self['HighIQ']/total:.0%} high. ({self['HighIQ']}/{total})")

    def __str__(self):
        return json.dumps(self)


def grab_rarities() -> Counter:
    time.sleep(0.75)
    color_cntr = Counter([kbs.grab_color((x, y)) for y in BUFF_POINTS_Y for x in BUFF_POINTS_X])
    rarity_cntr = RarityCounter(color_cntr)
    return rarity_cntr


def notify(*texts, webhook: str = None):
    for text in texts:
        cit.warn(text)
    if webhook:
        cct.ajax(webhook, {"text": "; ".join(texts)}, method="post")
    cit.pause()
    kbs.count_down(3)


def main():
    kbs.count_down(3)
    expansion = 0
    stat_cntr = StatisticsCounter(Rarity)
    while True:
        stat_cntr.print_iq_statistics(expansion * 10)
        stat_cntr.print_rarity_statistics()
        pbar = tqdm.tqdm(range(10), unit="round")
        for i in pbar:
            loop = expansion * 10 + i + 1
            pbar.set_postfix({
                "Loop": loop,
                "HighIQ": stat_cntr['HighIQ'],
            })
            pbar.set_description(f"Lv.{expansion}")
            kbs.left_mouse_button(REROLL_CLICK_POINT)
            time.sleep(1.25)
            high_attr_flag = kbs.grab_color(IQ_CHECK_POINT) != IQ_BACKGROUND_COLOR
            if not high_attr_flag and not RARITY_STATISTICS:
                continue
            else:
                rarity_cntr = grab_rarities()
                score = rarity_cntr.score(RARITY_WEIGHT)
                if score >= SCORE_EXTRAORDINARY:
                    notify(f"Qualified BUFFs detected! (Score: {score})", f"Rarity Counter: {rarity_cntr}", webhook=NOTIFY_WEBHOOK)
                if RARITY_STATISTICS:
                    stat_cntr += rarity_cntr
                if high_attr_flag:
                    # cit.warn("High IQ detected!")
                    stat_cntr['HighIQ'] += 1
                    if score >= SCORE_QUALIFIED:
                        notify(f"Qualified BUFFs detected! (Score: {score})", f"Rarity Counter: {rarity_cntr}", webhook=NOTIFY_WEBHOOK)
        expansion += 1


if __name__ == "__main__":
    main()
