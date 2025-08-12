from pathlib import Path
from pyqt_frameless_window import (Qt, QShortcut, QKeySequence, QTabWidget,
                                   QApplication, QVBoxLayout,QWidget)
from pyqt_frameless_window.size_grips import SizeGrips
from pyqt_frameless_window.title_bar import TitleBar
from ctypes import cast
from ctypes.wintypes import MSG
import win32con

from pyqt_frameless_window.utils import LPNCCALCSIZE_PARAMS, isMaximized


class FramelessWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.resize(500, 500)
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout.setContentsMargins(0, 5, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)

        self.titlebar = TitleBar(self)
        self._layout.addWidget(self.titlebar)

        self.body = QWidget()
        self.body_layout: QVBoxLayout = QVBoxLayout()
        self.body.setLayout(self.body_layout)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self.body)

        self.size_grips = SizeGrips(self)
        self.frameless_sc = QShortcut(QKeySequence('F11'), self,
                                      self.on_full_screen,
                                      context=Qt.ShortcutContext.ApplicationShortcut)

    def nativeEvent(self, eventType, message) -> tuple[bool, int]:  # type: ignore
        """ Handle the Windows message """
        msg = MSG.from_address(message.__int__())  # type: ignore
        if not msg.hWnd:
            return False, 0
        if msg.message == win32con.WM_NCCALCSIZE:
            rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]
            if isMaximized(msg.hWnd):
                if not self.isFullScreen():
                    rect.top += 5
                self.titlebar.set_maximized()
                self.size_grips.set_grips_visible(False)
            else:
                self.titlebar.set_normal()
                self.size_grips.set_grips_visible(not self.isFullScreen())
                rect.top -= 5
                rect.bottom -= 5
            return True, 0
        return False, 0

    def on_full_screen(self) -> None:
        if self.isFullScreen():
            self.showNormal()
            self.titlebar.setVisible(True)
        else:
            self.showFullScreen()
            self.titlebar.setVisible(False)
            self.size_grips.set_grips_visible(False)

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        self.size_grips.updateGrips()

    def add_center_widget(self, widget: QWidget) -> None:
        self.titlebar.center_layout.addWidget(widget)

    def add_right_widget(self, widget: QWidget) -> None:
        self.titlebar.right_layout.addWidget(widget)

    def add_left_widget(self, widget: QWidget) -> None:
        self.titlebar.left_layout.addWidget(widget)

    def setTitle(self, title: str) -> None:
        self.setWindowTitle(title)
        self.titlebar.title_label.text_label.setText(title)

    def title(self) -> str:
        return self.titlebar.title_label.text_label.text()

    def addWidget(self, w: QWidget):
        self.body_layout.addWidget(w)

    def set_icon(self, icon_path: str | Path):
        self.titlebar.title_label.set_icon(icon_path)


if __name__ == '__main__':
    app = QApplication([])
    w = FramelessWindow()

    f = QTabWidget(w)
    w.body_layout.addWidget(f)

    w.show()
    app.exec()