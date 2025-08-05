

import asyncio
from typing import Callable
import keyboard
from pyqt_frameless_window import QRect
from pyqt_frameless_window.snap_layout import ButtonKey, SnapState


class ShortcutsMixin:
    def __init__(self) -> None:
        keyboard.add_hotkey('left windows + left', self.on_shortcut,
                            args=(ButtonKey.LEFT, ), timeout=0.0)
        keyboard.add_hotkey('left windows + right', self.on_shortcut,
                            args=(ButtonKey.RIGHT, ), timeout=0.0)
        keyboard.add_hotkey('left windows + up', self.on_shortcut,
                            args=(ButtonKey.UP, ), timeout=0.0)
        keyboard.add_hotkey('left windows + down', self.on_shortcut,
                            args=(ButtonKey.DOWN, ), timeout=0.0)
        self.last_key: ButtonKey | None = None
        self.key_handler: Callable[[ButtonKey]] | None = None
        self.snap_state: SnapState = SnapState.NORMAL
        self._hidden_from: SnapState | None = None


    def on_shortcut(self, key: ButtonKey):
        self.last_key = key

    async def shortcuts_routine(self):
        while True:
            await asyncio.sleep(0.001)
            if self.last_key is not None:
                if self.key_handler:
                    self.key_handler(self.last_key)
                self.last_key = None

    def _save_geometry(self):
        ...

    def maximize(self):
        ...

    def normal(self):
        ...

    def setGeometry(self, rect):
        ...

    def set_visible(self, state: bool):
        ...

    def hide_grips(self):
        ...

    def get_current_screen(self) -> QRect:
        ...

    def set_snap_state(self, state: SnapState):
        g: QRect = self.get_current_screen()
        w: int = g.width()
        if self.snap_state == SnapState.NORMAL:
            self._save_geometry()
        if state == SnapState.MAXIMIZED:
            self.maximize()
            self.snap_state = state
            return
        if self._hidden_from and \
           (self._hidden_from == SnapState.BOTTOM_LEFT or \
            self._hidden_from == SnapState.BOTTOM_RIGHT):
               state = self._hidden_from
               self._hidden_from = None
        if state == SnapState.NORMAL:
            self.normal()
            self.snap_state = state
            return
        if state == SnapState.HIDDEN:
            self._hidden_from = self.snap_state
            self.snap_state = state
            self.setGeometry(QRect(0, 0, 0, 0))
            self.set_visible(False)
            return
        if state == SnapState.LEFT:
            g.setWidth(w // 2)
        elif state == SnapState.RIGHT:
            g.setX(w // 2)
            g.setWidth(w // 2)
        elif state == SnapState.TOP_LEFT:
            g.setWidth(w // 2)
            g.setHeight(g.height() // 2)
        elif state == SnapState.TOP_RIGHT:
            g.setX(w // 2)
            g.setWidth(w // 2)
            g.setHeight(g.height() // 2)
        elif state == SnapState.BOTTOM_LEFT:
            g.setWidth(w // 2)
            g.setY(g.height() // 2)
        elif state == SnapState.BOTTOM_RIGHT:
            g.setX(w // 2)
            g.setWidth(w // 2)
            g.setY(g.height() // 2)
        self.setGeometry(g)
        self.hide_grips()
        self.snap_state = state