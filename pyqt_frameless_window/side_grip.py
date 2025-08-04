from pyqt_frameless_window import Qt, QWidget



class SideGrip(QWidget):
    def __init__(self, parent, edge):
        QWidget.__init__(self, parent)
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        if edge == Qt.Edge.LeftEdge:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
            self.resizeFunc = self.resizeLeft
        elif edge == Qt.Edge.TopEdge:
            self.setCursor(Qt.CursorShape.SizeVerCursor)
            self.resizeFunc = self.resizeTop
        elif edge == Qt.Edge.RightEdge:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
            self.resizeFunc = self.resizeRight
        else:
            self.setCursor(Qt.CursorShape.SizeVerCursor)
            self.resizeFunc = self.resizeBottom
        self.mousePos = None

    def resizeLeft(self, delta):
        window = self.window()
        if window:
            width = max(window.minimumWidth(), window.width() - delta.x())
            geo = window.geometry()
            geo.setLeft(geo.right() - width)
            window.setGeometry(geo)

    def resizeTop(self, delta):
        window = self.window()
        if window:
            height = max(window.minimumHeight(), window.height() - delta.y())
            geo = window.geometry()
            geo.setTop(geo.bottom() - height)
            window.setGeometry(geo)

    def resizeRight(self, delta):
        window = self.window()
        if window:
            width = max(window.minimumWidth(), window.width() + delta.x())
            window.resize(width, window.height())

    def resizeBottom(self, delta):
        window = self.window()
        if window:
            height = max(window.minimumHeight(), window.height() + delta.y())
            window.resize(window.width(), height)

    def mousePressEvent(self, a0):
        if a0 and a0.button() == Qt.MouseButton.LeftButton:
            self.mousePos = a0.pos()

    def mouseMoveEvent(self, a0):
        if a0 and self.mousePos is not None:
            delta = a0.pos() - self.mousePos
            self.resizeFunc(delta)

    def mouseReleaseEvent(self, a0):
        self.mousePos = None

