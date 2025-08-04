import asyncio
from qasync import QEventLoop
from pyqt_frameless_window import (QWidget, QVBoxLayout, QPixmap, QPainter,
                                   QPalette, QApplication)



class Body(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)
        self.pixmap = QPixmap(self.size())
        self.resize(500, 500)

    def paintEvent(self, a0):
        super().paintEvent(a0)
        painter = QPainter(self)
        self.pixmap.fill(self.palette().color(QPalette.ColorRole.Window))
        painter.drawPixmap(0, 0, self.pixmap)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.pixmap = QPixmap(self.size())


if __name__ == '__main__':
    app = QApplication([])
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)
    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)
    w = Body()
    # f = QtWidgets.QTabWidget(w)
    # w.body_layout.addWidget(f)

    w.show()
    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())