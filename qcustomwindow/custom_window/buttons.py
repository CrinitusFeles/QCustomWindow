# coding:utf-8
from typing import Literal
from qcustomwindow import (QPointF, Qt, QColor, QPainter, QtCore,
                                   QPainterPath, QPen, QToolButton, QPalette)


class TitleBarButton(QToolButton):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setFixedSize(46, 32)
        self._state: Literal["normal", "hover", "pressed"] = "normal"

        self.setStyleSheet("""
            QToolButton{
                background-color: transparent;
                border: none;
                margin: 0px;
            }
        """)

    def _style(self):
        p = self.palette()
        return {
            "normal": {"color": p.color(QPalette.ColorRole.ButtonText), "background": '#00000000'},
            "hover": {"color": '#FFFFFF', "background": '#0064B6'},
            "pressed": {"color": '#FFFFFF', "background": '#363941'},
        }

    def setState(self, state: Literal["normal", "hover", "pressed"]):
        self._state = state
        self.update()

    def enterEvent(self, a0) -> None:
        self.setState("hover")
        super().enterEvent(a0)

    def leaveEvent(self, a0) -> None:
        self.setState("normal")
        super().leaveEvent(a0)

    def mousePressEvent(self, a0) -> None:
        if a0 and a0.button() != Qt.MouseButton.LeftButton:
            return

        self.setState("pressed")
        super().mousePressEvent(a0)

    def _init_painter(self) -> QPainter:
        painter = QPainter(self)
        # draw background
        style = self._style()[self._state]
        painter.setBrush(QColor(style["background"]))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())
        # draw icon
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(QColor(style["color"]), 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        return painter


class MinimizeButton(TitleBarButton):
    def paintEvent(self, a0) -> None:
        painter: QPainter = self._init_painter()
        painter.drawLine(18, 16, 28, 16)


class MaximizeButton(TitleBarButton):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._isMax: bool = False

    def setMaxState(self, isMax: bool) -> None:
        if self._isMax == isMax:
            return
        self._isMax = isMax
        self.setState("normal")

    def paintEvent(self, a0):
        painter: QPainter = self._init_painter()
        r: float = self.devicePixelRatioF()
        painter.scale(1 / r, 1 / r)
        if not self._isMax:
            painter.drawRect(int(18 * r), int(11 * r), int(10 * r), int(10 * r))
        else:
            painter.drawRect(int(18 * r), int(13 * r), int(8 * r), int(8 * r))
            x0: int = int(18 * r) + int(2 * r)
            y0: float = 13 * r
            dw = int(2 * r)
            path = QPainterPath(QPointF(x0, y0))
            path.lineTo(x0, y0 - dw)
            path.lineTo(x0 + 8 * r, y0 - dw)
            path.lineTo(x0 + 8 * r, y0 - dw + 8 * r)
            path.lineTo(x0 + 8 * r - dw, y0 - dw + 8 * r)
            painter.drawPath(path)


class CloseButton(TitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)

    def _style(self):
        p = self.palette()
        return {
            "normal": {"background": '#00000000', "color": p.color(QPalette.ColorRole.ButtonText)},
            "hover": {"background": '#E81123', "color": '#FFFFFF'},
            "pressed": {"background": '#F1707A', "color": '#FFFFFF'},
        }

    def paintEvent(self, a0) -> None:
        painter: QPainter = self._init_painter()
        r: float = self.devicePixelRatioF()
        painter.scale(1 / r, 1 / r)
        painter.drawLine(QtCore.QLineF(18 * r, 10 * r, 28 * r, 20 * r))
        painter.drawLine(QtCore.QLineF(18 * r, 20 * r, 28 * r, 10 * r))
