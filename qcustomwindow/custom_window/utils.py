import win32gui
from ctypes import POINTER, Structure, c_int
from ctypes.wintypes import HWND, RECT, UINT
import win32con


def isMaximized(hWnd: int):
    windowPlacement = win32gui.GetWindowPlacement(hWnd)
    if not windowPlacement:
        return False

    return windowPlacement[1] == win32con.SW_MAXIMIZE


class PWINDOWPOS(Structure):
    _fields_ = [
        ('hWnd',            HWND),
        ('hwndInsertAfter', HWND),
        ('x',               c_int),
        ('y',               c_int),
        ('cx',              c_int),
        ('cy',              c_int),
        ('flags',           UINT)
    ]


class NCCALCSIZE_PARAMS(Structure):
    _fields_ = [
        ('rgrc', RECT*3),
        ('lppos', POINTER(PWINDOWPOS))
    ]


LPNCCALCSIZE_PARAMS = POINTER(NCCALCSIZE_PARAMS)
