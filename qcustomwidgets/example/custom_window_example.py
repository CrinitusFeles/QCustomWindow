from pathlib import Path
from qcustomwidgets import (CustomWindow, QtWidgets, QMovie, QtGui,
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



class DemoWindow(CustomWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setTitle('Hello world')
        self.resize(700, 500)
        nyancat_label = QtWidgets.QLabel()
        assets = Path(__file__).parent / 'assets'
        movie = QMovie(str(assets / 'nyancat.gif'))
        nyancat_label.setMovie(movie)
        movie.start()
        self.add_left_widget(nyancat_label)

        version_button = QtWidgets.QPushButton(f'v.{__version__}')
        version_button.setMinimumWidth(60)
        version_button.setObjectName('version_button')
        version_button.setStyleSheet(round_button_stylesheet)
        self.add_right_widget(version_button)

        tab_widget = QtWidgets.QTabWidget()
        btn = QtWidgets.QPushButton('Push button')
        btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                          QtWidgets.QSizePolicy.Policy.Expanding)
        tab_widget.addTab(btn, 'Tab1')
        tab_widget.addTab(QtWidgets.QWidget(), 'Tab2')
        self.addWidget(tab_widget)

        self.dark_icon = QtGui.QIcon(str(assets / 'dark.svg'))
        self.light_icon = QtGui.QIcon(str(assets / 'light.svg'))
        self.style_button = QtWidgets.QPushButton()
        self.style_button.setIcon(self.dark_icon)
        self.style_button.setFlat(True)
        self.style_button.clicked.connect(self.on_change_style)
        self.add_right_widget(self.style_button)
        self.is_dark = True

    def on_change_style(self):
        if not self.is_dark:
            dark()
            self.style_button.setIcon(self.dark_icon)
        else:
            light()
            self.style_button.setIcon(self.light_icon)
        self.is_dark = not self.is_dark

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setStyleSheet(stylesheet)
    dark()
    w = DemoWindow()
    w.show()
    app.exec()