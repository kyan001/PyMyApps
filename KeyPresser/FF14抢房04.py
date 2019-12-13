import win32api
import win32con
import time
import random
import consoleiotools as cit

PREREQ = "站在门牌面前，不选中任何东西"
KEYS = {
    'num0': 0x60,
    'num1': 0x61,
    'num2': 0x62,
    'num3': 0x63,
    'num4': 0x64,
    'num5': 0x65,
    'num6': 0x66,
    'num7': 0x67,
    'num8': 0x68,
    'num9': 0x69,
}

def __press(key: str) -> bool:
    code = KEYS.get(key)
    if not code:
        cit.err(f'Key "{key}" does not exist.')
        return False
    cit.info(f'{key} pressed')
    win32api.keybd_event(code, 0, 0, 0)
    win32api.keybd_event(code, 0, win32con.KEYEVENTF_KEYUP, 0)
    return True

def __sleep(t: float, mute: bool=False):
    if not mute:
        cit.info(f"{int(t*1000)}ms sleeped")
    time.sleep(t)

def before_start():
    cit.info(f"Pre Requirement: {PREREQ}")

def count_down():
    cit.info("3 ...")
    __sleep(1, mute=True)
    cit.info("2 ...")
    __sleep(1, mute=True)
    cit.info("1 ...")
    __sleep(1, mute=True)
    cit.info("GO")

def start():
    before_start()
    count_down()
    __press('num0')
    __sleep(random.random() + 1)
    for i in range(1, 1000000):
        __press('num0')
        __sleep(random.random() * 0.5 + 0.5)
        __press('num0')
        __sleep(random.random() * 3 + 1)
        __press('num0')
        __sleep(random.random() * 0.5 + 0.3)
        __press('num0')
        __sleep(random.random() * 0.5 + 0.3)
        __press('num4')
        __sleep(random.random() * 0.5 + 0.3)
        __press('num0')
        __sleep(random.random() * 0.5 + 0.3)
        cit.info(f"{i}th round done, resting")
        __sleep(random.random() + 2)

if __name__ == '__main__':
    start()
