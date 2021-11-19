import sys
import io

from PySide2 import QtCore, QtWidgets, QtGui
from PIL import Image

from converter import convert, resize


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_image_open = False

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

        # Status Bar
        self.status = self.statusBar()

        # Window dimensions
        self.geometry = qApp.desktop().availableGeometry(self)
        self.computedWidth = self.geometry.width() * 0.5
        self.computedHeight = self.geometry.height() * 0.5
        self.setFixedSize(self.computedWidth, self.computedHeight)

        # Layout
        window = QtWidgets.QWidget()

        self.label = QtWidgets.QLabel(parent=self)
        self.textedit = QtWidgets.QTextEdit()

        self.label.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored
        )

        self.preview_btn = QtWidgets.QPushButton('Preview')
        self.preview_btn.clicked.connect(self.preview)
        self.convert_btn = QtWidgets.QPushButton('Convert')
        self.convert_btn.clicked.connect(self.get_bytes)
        # Disable those buttons at start
        self.preview_btn.setDisabled(True)
        self.convert_btn.setDisabled(True)

        layout_skeleton = QtWidgets.QVBoxLayout()

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.label, stretch=1)
        top_layout.addWidget(self.textedit, stretch=1)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.preview_btn)
        button_layout.addWidget(self.convert_btn)

        layout_skeleton.addLayout(top_layout)
        layout_skeleton.addLayout(button_layout)

        window.setLayout(layout_skeleton)
        self.setCentralWidget(window)

    @QtCore.Slot()
    def get_bytes(self):
        try:
            img_bytearray = convert(self.filename)
            self.textedit.setText(img_bytearray)
        except Exception as e:
            self.status.showMessage(f'{e}')
        else:
            self.status.showMessage(f'Converted {self.filename} to byte array')

    @QtCore.Slot()
    def preview(self):
        self.preview_btn.setDisabled(True)
        try:
            pixmap = resize(self.filename)
            self.label.setPixmap(pixmap)
        except Exception as e:
            self.status.showMessage(f'{e}')
        else:
            self.status.showMessage(f'Previewing {self.filename} as 1-bit bitmap')

    @QtCore.Slot()
    def open_file_dialog(self):
        self.filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open Image', '.', 'Image Files (*.png *.jpg *.jpeg *.bmp)'
        )

        self.textedit.clear()

        pixmap = QtGui.QPixmap(self.filename)
        pixmap_w, pixmap_h = pixmap.size().width(), pixmap.size().height()
        if not (pixmap_w < self.computedWidth and pixmap_h < self.computedHeight):
            pixmap = pixmap.scaled(self.computedWidth, self.computedHeight, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.status.showMessage(f'{self.filename} loaded successfully')
        self.preview_btn.setDisabled(False)
        self.convert_btn.setDisabled(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
