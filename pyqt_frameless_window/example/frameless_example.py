import asyncio
from pathlib import Path
from qasync import QEventLoop
from pyqt_frameless_window import (FramelessWindow, QtWidgets, QMovie,
                                   __version__, dark, light, stylesheet)  # noqa: F401


round_button_stylesheet = """
#version_button{
    border-radius: 10px;
    border-style: outset;
    border-width: 2px;
}
#version_button::hover {
    background-color: #454545;
}
#version_button::pressed {
    background-color: #242424;
}
"""


class DemoWindow(FramelessWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.titlebar.setTitle('Hello world')
        self.setStyleSheet(stylesheet)
        nyancat_label = QtWidgets.QLabel()
        movie = QMovie(str(Path(__file__).parent / 'assets' / 'nyancat.gif'))
        nyancat_label.setMovie(movie)
        movie.start()
        self.titlebar.add_left_widget(nyancat_label)

        version_button = QtWidgets.QPushButton(f'v.{__version__}')
        version_button.setMinimumWidth(60)
        version_button.setObjectName('version_button')
        version_button.setStyleSheet(round_button_stylesheet)
        self.titlebar.add_right_widget(version_button)

        tab_widget = QtWidgets.QTabWidget()
        btn = QtWidgets.QPushButton('Push button')
        btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                          QtWidgets.QSizePolicy.Policy.Expanding)
        tab_widget.addTab(btn, 'Tab1')
        tab_widget.addTab(QtWidgets.QWidget(), 'Tab2')
        self.body_layout.addWidget(tab_widget)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)
    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)
    dark()
    w = DemoWindow()
    w.show()
    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())