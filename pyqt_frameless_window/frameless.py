from pyqt_frameless_window import (Qt, QPoint, QShortcut, QKeySequence,
                                   QApplication, QVBoxLayout,
                                   QTabWidget, QWidget)
from pyqt_frameless_window.size_grips import SizeGrips
from pyqt_frameless_window.title_bar import TitleBar
from ctypes import cast
from ctypes.wintypes import LPRECT, MSG
import win32con

from pyqt_frameless_window.utils import LPNCCALCSIZE_PARAMS, isMaximized


class FramelessWindow(QWidget):
    BORDER_WIDTH = 10
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.frameless_sc = QShortcut(QKeySequence('F11'), self,
                                      self.on_full_screen,
                                      context=Qt.ShortcutContext.ApplicationShortcut)

        self.resize(500, 500)
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)
        self.titlebar = TitleBar(self)
        self.titlebar.maxButton.clicked.connect(self.on_maximize)
        self.titlebar.window_moved.connect(self.on_move)
        self._layout.addWidget(self.titlebar)

        self.body = QWidget()
        self.body_layout: QVBoxLayout = QVBoxLayout()
        self.body.setLayout(self.body_layout)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self.body)

        self.size_grips = SizeGrips(self)

    def nativeEvent(self, eventType, message): # type: ignore
        """ Handle the Windows message """
        msg = MSG.from_address(message.__int__())  # type: ignore
        self.hwnd = msg.hWnd
        if not msg.hWnd:
            return False, 0
        if msg.message == win32con.WM_NCCALCSIZE:
            if msg.wParam:
                c = cast(msg.lParam, LPNCCALCSIZE_PARAMS)
                rect = c.contents.rgrc[0]
                if isMaximized(msg.hWnd) or self.isFullScreen():
                    if not self.isFullScreen():
                        rect.top += 5
                    self.titlebar.set_maximized()
                    self.size_grips.set_grips_visible(False)
                else:
                    self.titlebar.set_normal()
                    self.size_grips.set_grips_visible(True)
                    rect.top -= 5
                    rect.bottom -= 5
            else:
                rect = cast(msg.lParam, LPRECT).contents
            return True, 0
        return False, 0

    def on_full_screen(self):
        if self.isFullScreen():
            self.showNormal()
            self.titlebar.setVisible(True)
        else:
            self.showFullScreen()
            self.titlebar.setVisible(False)

    def on_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def on_move(self, movement: QPoint):
        _ = self.windowHandle().startSystemMove()  # type: ignore

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.size_grips.updateGrips()


if __name__ == '__main__':
    app = QApplication([])
    w = FramelessWindow()

    f = QTabWidget(w)
    w.body_layout.addWidget(f)

    w.show()
    app.exec()