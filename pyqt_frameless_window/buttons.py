# coding:utf-8
from pathlib import Path
from typing import Literal
from pyqt_frameless_window import (QPointF, QSize, Qt, QColor, QIcon, QPainter,
                                   QPainterPath, QPen, QToolButton)


class TitleBarButton(QToolButton):
    def __init__(self, style=None, parent=None):
        """
        Parameters
        ----------
        style: dict
            button style of `normal`,`hover`, and `pressed`. Each state has
            `color`, `background` and `icon`(close button only) attributes.

        parent:
            parent widget
        """
        super().__init__(parent=parent)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setFixedSize(46, 32)
        self._state = "normal"
        self._style = {
            "normal": {"color": '#000000', "background": '#00000000'},
            "hover": {"color": '#FFFFFF', "background": '#0064B6'},
            "pressed": {"color": '#FFFFFF', "background": '#363941'},
        }
        self.updateStyle(style)
        self.setStyleSheet("""
            QToolButton{
                background-color: transparent;
                border: none;
                margin: 0px;
            }
        """)

    def updateStyle(self, style):
        style = style or {}
        for k, v in style.items():
            self._style[k].update(v)

        self.update()

    def setState(self, state: Literal["normal", "hover", "pressed"]):
        self._state = state
        self.update()

    def enterEvent(self, a0):
        self.setState("hover")
        super().enterEvent(a0)

    def leaveEvent(self, a0):
        self.setState("normal")
        super().leaveEvent(a0)

    def mousePressEvent(self, a0):
        if a0 and a0.button() != Qt.MouseButton.LeftButton:
            return

        self.setState("pressed")
        super().mousePressEvent(a0)


class MinimizeButton(TitleBarButton):
    def paintEvent(self, a0):
        painter = QPainter(self)

        # draw background
        style = self._style[self._state]
        painter.setBrush(QColor(style["background"]))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(QColor(style["color"]), 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(18, 16, 28, 16)


class MaximizeButton(TitleBarButton):
    def __init__(self, style=None, parent=None):
        super().__init__(style, parent)
        self.__isMax: bool = False

    def setMaxState(self, isMax: bool):
        """update the maximized state and icon"""
        if self.__isMax == isMax:
            return

        self.__isMax = isMax
        self.setState("normal")

    def paintEvent(self, a0):
        painter = QPainter(self)

        # draw background
        style: dict[str, str] = self._style[self._state]
        painter.setBrush(QColor(style["background"]))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(QColor(style["color"]), 1)
        pen.setCosmetic(True)
        painter.setPen(pen)

        r: float = self.devicePixelRatioF()
        painter.scale(1 / r, 1 / r)
        if not self.__isMax:
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
    def __init__(self, style=None, parent=None):
        black_icon = str(Path(__file__).parent / "assets" / "close_black.svg")
        white_icon = str(Path(__file__).parent / "assets" / "close_white.svg")
        defaultStyle: dict[str, dict[str, str]] = {
            "normal": {"background": '#00000000', "icon": black_icon},
            "hover": {"background": '#E81123', "icon": white_icon},
            "pressed": {"background": '#F1707A', "icon": white_icon},
        }
        super().__init__(defaultStyle, parent)
        self.updateStyle(style)
        self.setIconSize(QSize(46, 32))
        self.setIcon(QIcon(self._style["normal"]["icon"]))

    def updateStyle(self, style):
        super().updateStyle(style)
        self.setIcon(QIcon(self._style[self._state]["icon"]))

    def enterEvent(self, a0):
        self.setIcon(QIcon(self._style["hover"]["icon"]))
        super().enterEvent(a0)

    def leaveEvent(self, a0):
        self.setIcon(QIcon(self._style["normal"]["icon"]))
        super().leaveEvent(a0)

    def mousePressEvent(self, a0):
        self.setIcon(QIcon(self._style["pressed"]["icon"]))
        super().mousePressEvent(a0)

    def mouseReleaseEvent(self, a0):
        self.setIcon(QIcon(self._style["normal"]["icon"]))
        super().mouseReleaseEvent(a0)

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # draw background
        style: dict[str, str] = self._style[self._state]
        painter.setBrush(QColor(style["background"]))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        super().paintEvent(a0)
