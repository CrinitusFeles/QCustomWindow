from pyqt_frameless_window import QSizeGrip, QWidget, QRect, QPoint, Qt
from pyqt_frameless_window.side_grip import SideGrip


class SizeGrips:
    def __init__(self, parent: QWidget, grip_size: int = 10):
        self.parent_obj = parent
        self.sideGrips = [
            SideGrip(self.parent_obj, Qt.Edge.LeftEdge),
            SideGrip(self.parent_obj, Qt.Edge.TopEdge),
            SideGrip(self.parent_obj, Qt.Edge.RightEdge),
            SideGrip(self.parent_obj, Qt.Edge.BottomEdge),
        ]
        self.cornerGrips: list[QSizeGrip] = [QSizeGrip(parent) for _ in range(4)]
        self.corner_grip_size = grip_size
        self.gripSize = grip_size
        for corner in self.cornerGrips:
            corner.setStyleSheet("background-color: transparent; ")

    def set_grips_visible(self, state: bool):
        for grip in [*self.sideGrips, *self.cornerGrips]:
            grip.setVisible(state)

    def updateGrips(self):
        outRect = self.parent_obj.rect()

        # top left
        self.cornerGrips[0].setGeometry(
            # QtCore.QRect(outRect.topLeft(), inRect.topLeft()))
            QRect(outRect.topLeft(),
                         outRect.topLeft() + QPoint(self.corner_grip_size,
                                                    self.corner_grip_size))
        )
        # top right
        self.cornerGrips[1].setGeometry(
            # QtCore.QRect(outRect.topRight(), inRect.topRight()).normalized())
            QRect(outRect.topRight(),
                         outRect.topRight() + QPoint(-self.corner_grip_size,
                                                     self.corner_grip_size)).normalized()
        )
        # bottom right
        self.cornerGrips[2].setGeometry(
            # QtCore.QRect(inRect.bottomRight(), outRect.bottomRight()))
            QRect(outRect.bottomRight() + QPoint(-self.corner_grip_size,
                                                        -self.corner_grip_size),
                         outRect.bottomRight())
        )
        # bottom left
        self.cornerGrips[3].setGeometry(
            # QtCore.QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())
            QRect(outRect.bottomLeft() + QPoint(self.corner_grip_size,
                                                       -self.corner_grip_size),
                         outRect.bottomLeft()).normalized()
        )
        # left edge
        self.sideGrips[0].setGeometry(
            0,
            self.corner_grip_size,
            self.gripSize,
            outRect.height() - self.corner_grip_size
        )
        # top edge
        self.sideGrips[1].setGeometry(
            self.corner_grip_size,
            0,
            outRect.width() - self.corner_grip_size,
            self.gripSize
        )
        # right edge
        self.sideGrips[2].setGeometry(
            outRect.width() - self.gripSize,
            self.corner_grip_size,
            self.gripSize,
            outRect.height() - self.corner_grip_size
        )
        # bottom edge
        self.sideGrips[3].setGeometry(
            self.corner_grip_size,
            outRect.height() - self.gripSize,
            outRect.width() - self.corner_grip_size,
            self.gripSize
        )