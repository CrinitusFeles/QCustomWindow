from pyqt_frameless_window import (Qt, QPoint, QRect, QTimer, QCursor,
                                   QShortcut, QKeySequence, QPixmap, QPainter,
                                   QColor, QApplication, QWidget, QVBoxLayout,
                                   QTabWidget)
from pyqt_frameless_window.body import Body
from pyqt_frameless_window.size_grips import SizeGrips
from pyqt_frameless_window.shortcuts_mixin import ShortcutsMixin
from pyqt_frameless_window.title_bar import TitleBar
from pyqt_frameless_window.snap_layout import ButtonKey, snap_states, SnapState


class FramelessWindow(QWidget, ShortcutsMixin):
    BORDER_WIDTH = 10
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.frameless_sc = QShortcut(QKeySequence('F11'), self,
                                      self.on_full_screen,
                                      context=Qt.ShortcutContext.ApplicationShortcut)
        self.pixmap = QPixmap(self.size())
        self.pixmap.fill(QColor(0, 0, 0, 1))

        self.resize(500, 500)
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout.setContentsMargins(self.BORDER_WIDTH, self.BORDER_WIDTH,
                                        self.BORDER_WIDTH, self.BORDER_WIDTH)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)

        self.titlebar = TitleBar(self)
        self.titlebar.setObjectName('titlebar')
        self.titlebar.maxButton.clicked.connect(self.on_maximize)
        self.titlebar.window_moved.connect(self.on_move)
        self._layout.addWidget(self.titlebar)

        self.body = Body()
        self.body.setObjectName('body')
        self.body_layout: QVBoxLayout = self.body._layout
        self._layout.addWidget(self.body)

        self.size_grips = SizeGrips(self)

        self._last_geom: QRect = self.geometry()
        self.win_key_timer = QTimer()
        self.win_key_timer.timeout.connect(self.shortcuts_routine)
        self.win_key_timer.start(1)
        self.key_handler = self.on_win

    def set_visible(self, state: bool):
        self.titlebar.setVisible(state)
        self.body.setVisible(state)

    def hide_grips(self):
        self.size_grips.set_grips_visible(False)
        self._layout.setContentsMargins(0, 0, 0, 0)

    def on_win(self, key: ButtonKey):
        if self.isActiveWindow() and not self.isFullScreen():
            state: SnapState = snap_states.get((self.snap_state, key),
                                               self.snap_state)
            if not self.titlebar.isVisible():
                self.set_visible(True)
            self.set_snap_state(state)
            if not self._is_maximized():
                self.titlebar.set_normal()

    def _is_maximized(self):
        return self.snap_state == SnapState.MAXIMIZED

    def on_full_screen(self):
        if not self.isFullScreen():
            if self.snap_state == SnapState.NORMAL:
                self._save_geometry()
            self.fullscreen()
        else:
            if self._is_maximized():
                self.maximize()
            else:
                show_grips = self.snap_state == SnapState.NORMAL
                self.normal(set_state=False, show_grips=show_grips)
            self.titlebar.setVisible(True)

    def move_to_cursor(self):
        if self.titlebar.pressing:
            pos: QPoint = QCursor.pos()
            self.move(pos.x() - self.width() // 2,
                      pos.y() - self.BORDER_WIDTH * 2)

    def fullscreen(self):
        self.showFullScreen()
        self.titlebar.setVisible(False)
        self.hide_grips()

    def on_maximize(self):
        if self._is_maximized():
            self.normal()
        else:
            self.maximize()

    def maximize(self):
        if self._is_maximized():
            return
        if self.snap_state == SnapState.NORMAL:
            self._save_geometry()
        self.showMaximized()
        self.titlebar.set_maximized()
        self.hide_grips()
        self.snap_state = SnapState.MAXIMIZED

    def get_current_screen(self):
        screen = QApplication.screenAt(self.pos())
        if not screen:
            raise RuntimeError('Screen not found')
        g = screen.availableGeometry()
        return g

    def showMaximized(self):
        g = self.get_current_screen()
        self.setGeometry(g)

    def normal(self, set_state: bool = True, show_grips: bool = True):
        self.showNormal()
        self.titlebar.set_normal()
        if show_grips:
            self.size_grips.set_grips_visible(True)
            self._layout.setContentsMargins(self.BORDER_WIDTH, self.BORDER_WIDTH,
                                            self.BORDER_WIDTH, self.BORDER_WIDTH)
        if set_state:
            self.setGeometry(self._last_geom)
            self.snap_state = SnapState.NORMAL

    def paintEvent(self, a0):
        super().paintEvent(a0)
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)

    def on_move(self, movement: QPoint):
        if self._is_maximized():
            self.normal()
            self.move_to_cursor()
        if self.y() > self.BORDER_WIDTH:
            y: int = self.mapToGlobal(movement).y()
        elif movement.y() <= 0:
            y = -self.BORDER_WIDTH
        else:
            y = self.y() + movement.y()
        self.setGeometry(self.mapToGlobal(movement).x(),
                         y,
                         self.width(),
                         self.height())

        if self.snap_state != SnapState.NORMAL:
            self.normal()
            self.move_to_cursor()
        self._save_geometry()

    def _save_geometry(self):
        self._last_geom = self.geometry()

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.size_grips.updateGrips()
        self.pixmap = QPixmap(self.size())
        self.pixmap.fill(QColor(0, 0, 0, 1))


if __name__ == '__main__':
    app = QApplication([])
    w = FramelessWindow()

    f = QTabWidget(w)
    w.body_layout.addWidget(f)

    w.show()
    app.exec()