import sys

from PySide2 import QtCore, QtWidgets, QtGui
from converter import convert


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Eartquakes information')

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu('File')

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

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage('Get byte array')

        # Window dimensions
        geometry = qApp.desktop().availableGeometry(self)
        self.setFixedSize(geometry.width() * 0.5, geometry.height() * 0.5)

    @QtCore.Slot()
    def open_file_dialog(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open Image', '.', 'Image Files (*.png *.jpg *.jpeg *.bmp)'
        )

        # geometry = qApp.desktop().availableGeometry(self)
        # bytestr = convert(filename)
        # textbox = QtWidgets.QTextEdit(bytestr, self)
        # textbox.setLineWrapMode(QtWidgets.QTextEdit.FixedPixelWidth)
        # textbox.setLineWrapColumnOrWidth(geometry.width() * 0.25)
        # self.setCentralWidget(textbox)

        label = QtWidgets.QLabel(parent=self)
        pixmap = QtGui.QPixmap(filename)
        label.setPixmap(pixmap)
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.setCentralWidget(label)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
