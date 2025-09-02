from pathlib import Path
from qcustomwindow import (Qt, QPoint, QMouseEvent, QWidget, Signal,
                                   QHBoxLayout, QLabel, QPixmap, QApplication)
from qcustomwindow.buttons import CloseButton, MaximizeButton, MinimizeButton


class LabelIcon(QWidget):
    def __init__(self, text: str = '', icon_path: Path | str | None = None) -> None:
        super().__init__()
        self.icon_label = QLabel()
        if isinstance(icon_path, Path):
            icon_path = str(icon_path)
        if icon_path:
            self.pixmap = QPixmap(icon_path)
        else:
            self.pixmap = QPixmap()
        self.icon_label.setPixmap(self.pixmap)
        self.setMaximumHeight(25)
        self.text_label = QLabel(text)
        self._layout = QHBoxLayout()
        self._layout.addWidget(self.icon_label)
        self._layout.addWidget(self.text_label)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

    def set_icon(self, icon_path: Path | str) -> None:
        print(self.pixmap.load(str(icon_path)))
        self.icon_label.setPixmap(self.pixmap)

    def resizeEvent(self, a0):
        if self.pixmap.isNull():
            return
        w, h = self.width(), self.height()
        t = Qt.TransformationMode.SmoothTransformation
        k = Qt.AspectRatioMode.KeepAspectRatio
        pixmap = self.pixmap.scaled(w, h, transformMode=t,
                                                    aspectRatioMode=k)
        self.icon_label.setPixmap(pixmap)


class TitleBar(QWidget):
    window_moved: Signal = Signal(QPoint)
    def __init__(self, parent: QWidget, title="") -> None:
        super().__init__(parent)
        self.parent_obj: QWidget = parent
        self.setFixedHeight(32)
        parent.setWindowTitle(title)

        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)
        self.left_layout = QHBoxLayout()
        self.left_layout.setContentsMargins(10, 0, 0, 0)
        self.center_layout = QHBoxLayout()
        self.center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.center_layout.setSpacing(10)
        self._layout.setStretchFactor(self.center_layout, 1)
        self.right_layout = QHBoxLayout()
        self.left_layout.setSpacing(15)
        self.right_layout.setSpacing(10)
        self.right_layout.setContentsMargins(0, 0, 15, 0)
        self._layout.addLayout(self.left_layout)
        self._layout.addLayout(self.center_layout, 1)
        self._layout.addLayout(self.right_layout)
        self.title_label = LabelIcon(title)
        self.center_layout.addWidget(self.title_label)
        self.closeButton = CloseButton()
        self.maxButton = MaximizeButton()
        self.minButton = MinimizeButton()
        self.center_layout.setContentsMargins(self.closeButton.width() * 3,
                                              0, 0, 0)

        self.closeButton.clicked.connect(QApplication.closeAllWindows)
        self.minButton.clicked.connect(parent.showMinimized)
        self.maxButton.clicked.connect(self.set_maximized)
        self._layout.addWidget(self.minButton,
                               alignment=Qt.AlignmentFlag.AlignRight)
        self._layout.addWidget(self.maxButton)
        self._layout.addWidget(self.closeButton)
        self.pressing: bool = False
        self._start: QPoint = QPoint(0, 0)

    def set_maximized(self) -> None:
        self.maxButton.setMaxState(True)
        self.on_maximize()

    def on_maximize(self) -> None:
        if self.parent_obj.isMaximized():
            self.parent_obj.showNormal()
        else:
            self.parent_obj.showMaximized()

    def set_normal(self) -> None:
        self.maxButton.setMaxState(False)

    def mouseDoubleClickEvent(self, a0: QMouseEvent | None) -> None:
        self.maxButton.clicked.emit()
        return super().mouseDoubleClickEvent(a0)

    def mousePressEvent(self, a0: QMouseEvent | None):
        if a0:
            pos: QPoint = a0.pos()
            if pos.x() < self.parent_obj.width():
                self._start = self.mapToGlobal(a0.pos())
                self.pressing = True

    def mouseReleaseEvent(self, a0: QMouseEvent | None):
        self.pressing = False

    def mouseMoveEvent(self, a0: QMouseEvent | None) -> None:
        if a0 and self.pressing:
            end: QPoint = self.mapToGlobal(a0.pos())
            movement: QPoint = end - self._start  # noqa: F841
            self._start = end
            # self.window_moved.emit(movement)
            self.parent_obj.windowHandle().startSystemMove()  # type: ignore
