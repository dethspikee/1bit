import sys

from PySide2 import QtCore, QtWidgets, QtGui
from converter import convert


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('1bit')

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu('File')

        # Disable context menu for main window
        self.setContextMenuPolicy(QtGui.Qt.PreventContextMenu)

        # Open QAction
        open_action = QtWidgets.QAction('Open', self)
        open_action.setShortcut(QtGui.QKeySequence.Quit)
        open_action.triggered.connect(self.open_file_dialog)

        # Exit QAction
        exit_action = QtWidgets.QAction('Exit', self)
        exit_action.setShortcut(QtGui.QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        self.file_menu.addAction(open_action)
        self.file_menu.addAction(exit_action)

        # Toolbar
        toolbar = QtWidgets.QToolBar(self)
        self.addToolBar(toolbar)

        # Status Bar
        self.status = self.statusBar()

        # Window dimensions
        geometry = qApp.desktop().availableGeometry(self)
        self.setFixedSize(geometry.width() * 0.5, geometry.height() * 0.5)

        # Layout
        window = QtWidgets.QWidget()
        self.label = QtWidgets.QLabel(parent=self)
        self.preview_btn = QtWidgets.QPushButton('Preview')

        layout = QtWidgets.QGridLayout()

        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.preview_btn, 1, 0)

        window.setLayout(layout)
        self.setCentralWidget(window)

    @QtCore.Slot()
    def open_file_dialog(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open Image', '.', 'Image Files (*.png *.jpg *.jpeg *.bmp)'
        )

        pixmap = QtGui.QPixmap(filename)
        self.label.setPixmap(pixmap)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.status.showMessage( f'{filename} loaded successfully')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
