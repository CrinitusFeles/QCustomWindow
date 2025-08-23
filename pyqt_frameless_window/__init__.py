__version__ = '0.3.2'

try:
    from PyQt6.QtCore import QPointF, QSize, Qt, QPoint, QRect, QTimer, QEvent
    from PyQt6.QtGui import (QColor, QIcon, QPainter, QPainterPath, QPen,
                             QPalette, QPixmap, QCursor, QShortcut, QRegion,
                             QKeySequence, QMouseEvent, QMovie, QWindow)
    from PyQt6.QtWidgets import (QToolButton, QWidget, QApplication,
                                 QVBoxLayout, QTabWidget, QSizeGrip,
                                 QHBoxLayout, QLabel)
    from PyQt6.QtCore import pyqtSignal as Signal
    from PyQt6 import QtWidgets, QtGui, QtCore
except ImportError:
    from PySide6.QtCore import (QPointF, QSize, Qt, QPoint, QRect, QTimer,  # noqa: F401
                                Signal, QEvent)
    from PySide6.QtGui import (QColor, QIcon, QPainter, QPainterPath, QPen,  # noqa: F401
                               QPalette, QPixmap, QCursor, QShortcut, QWindow,
                               QKeySequence, QMouseEvent, QMovie, QRegion)
    from PySide6.QtWidgets import (QToolButton, QWidget, QApplication,  # noqa: F401
                                   QVBoxLayout, QTabWidget, QSizeGrip,
                                   QHBoxLayout, QLabel)
    from PySide6 import QtWidgets, QtGui, QtCore  # noqa: F401
from .frameless import FramelessWindow  # noqa: F401
from .style.palettes import dark, light  # noqa: F401
from .style.stylesheets import stylesheet  # noqa: F401