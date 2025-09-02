__version__ = '0.3.3'

try:
    from PyQt6.QtCore import (QPointF, QSize, Qt, QPoint, QRect, QTimer, QEvent,
                              QEasingCurve, QPropertyAnimation)
    from PyQt6.QtGui import (QColor, QIcon, QPainter, QPainterPath, QPen, QImage,
                             QPalette, QPixmap, QCursor, QShortcut, QRegion,
                             QKeySequence, QMouseEvent, QMovie, QWindow, QBrush)
    from PyQt6.QtWidgets import (QToolButton, QWidget, QApplication,
                                 QVBoxLayout, QTabWidget, QSizeGrip, QCheckBox,
                                 QHBoxLayout, QLabel, QAbstractButton,
                                 QGraphicsDropShadowEffect, QStackedLayout)
    from PyQt6.QtSvg import QSvgRenderer
    from PyQt6.QtCore import pyqtSignal as Signal
    from PyQt6 import QtWidgets, QtGui, QtCore
except ImportError:
    from PySide6.QtCore import (QPointF, QSize, Qt, QPoint, QRect, QTimer,  # noqa: F401
                                Signal, QEvent, QEasingCurve, QPropertyAnimation,
                                Property, Slot)
    from PySide6.QtSvg import QSvgRenderer  # noqa: F401
    from PySide6.QtGui import (QColor, QIcon, QPainter, QPainterPath, QPen,  # noqa: F401
                               QPalette, QPixmap, QCursor, QShortcut, QWindow, QImage,
                               QKeySequence, QMouseEvent, QMovie, QRegion, QBrush,
                               )
    from PySide6.QtWidgets import (QToolButton, QWidget, QApplication,  # noqa: F401
                                   QVBoxLayout, QTabWidget, QSizeGrip, QCheckBox,
                                   QHBoxLayout, QLabel, QAbstractButton,
                                   QGraphicsDropShadowEffect, QStackedLayout)
    from PySide6 import QtWidgets, QtGui, QtCore  # noqa: F401
from .custom_window.window import CustomWindow  # noqa: F401
from .style.palettes import dark, light  # noqa: F401
from .style.stylesheets import stylesheet  # noqa: F401