from pyqt_frameless_window import Qt, QPoint, QMouseEvent, QWidget, Signal, QHBoxLayout, QLabel
from pyqt_frameless_window.buttons import (CloseButton, MaximizeButton,
                                           MinimizeButton)


class TitleBar(QWidget):
    window_moved: Signal = Signal(QPoint)
    def __init__(self, parent: QWidget, title="") -> None:
        super().__init__(parent)
        self.parent_obj: QWidget = parent
        self.setFixedHeight(32)
        parent.setWindowTitle(title)
        self.setStyleSheet('background-color: palette(Window);')
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)
        self.left_layout = QHBoxLayout()
        self.center_layout = QHBoxLayout()
        self.center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_layout = QHBoxLayout()
        self.left_layout.setSpacing(15)
        self.right_layout.setSpacing(10)
        self.right_layout.setContentsMargins(0, 0, 15, 0)
        self._layout.addLayout(self.left_layout)
        self._layout.addLayout(self.center_layout, 1)
        self._layout.addLayout(self.right_layout)
        self.right_layout.addStretch()
        self.title_label = QLabel(title)
        self.center_layout.addWidget(self.title_label)
        self.closeButton = CloseButton()
        self.maxButton = MaximizeButton()
        self.minButton = MinimizeButton()
        self.center_layout.setContentsMargins(self.closeButton.width() * 3,
                                              0, 0, 0)
        self.center_layout.setSpacing(10)

        self.closeButton.clicked.connect(parent.close)
        self.minButton.clicked.connect(parent.showMinimized)
        self.maxButton.clicked.connect(self.set_maximized)
        self._layout.addWidget(self.minButton,
                               alignment=Qt.AlignmentFlag.AlignRight)
        self._layout.addWidget(self.maxButton)
        self._layout.addWidget(self.closeButton)
        self.pressing: bool = False
        self.anims = list()
        self._start: QPoint = QPoint(0, 0)
        self.window().installEventFilter(self)  # type: ignore

    def set_maximized(self) -> None:
        self.maxButton.setMaxState(True)

    def set_normal(self) -> None:
        self.maxButton.setMaxState(False)

    def mouseDoubleClickEvent(self, a0: QMouseEvent | None) -> None:
        self.maxButton.clicked.emit()
        return super().mouseDoubleClickEvent(a0)

    def add_center_widget(self, widget: QWidget) -> None:
        self.center_layout.addWidget(widget)

    def add_right_widget(self, widget: QWidget) -> None:
        self.right_layout.addWidget(widget)

    def add_left_widget(self, widget: QWidget) -> None:
        self.left_layout.addWidget(widget)

    def setTitle(self, title: str) -> None:
        self.parent_obj.setWindowTitle(title)
        self.title_label.setText(title)

    def title(self) -> str:
        return self.title_label.text()

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
            movement: QPoint = end - self._start
            self._start = end
            self.window_moved.emit(movement)

