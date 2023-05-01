import time
import win32api
import win32con

from PIL import ImageGrab
import consoleiotools as cit

__version__ = "1.1.1"


def dpi_enable(level: int = 2):
    import ctypes
    try:  # Win8, Win10
        ctypes.windll.shcore.SetProcessDpiAwareness(level)
    except:  # Win7
        ctypes.windll.user32.SetProcessDPIAware()


@cit.as_session
def count_down(num: int):
    for i in range(num, 0, -1):
        cit.info(f"{i}...")
        time.sleep(1)


def grab_color(pos: tuple[int, int] = None, size: int = 1, show: bool = False):
    """Grab the color of given pixel"""
    pos = pos or win32api.GetCursorPos()
    pixel = ImageGrab.grab((pos[0], pos[1], pos[0] + size, pos[1] + size))
    return pixel.load()[0, 0] if not show else pixel.show()


def get_cursor_pos():
    return win32api.GetCursorPos()


def left_mouse_button(pos: tuple[int, int] = None):
    """Simulate a left mouse button click"""
    if pos:
        win32api.SetCursorPos(pos)
        time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.1)


dpi_enable()
