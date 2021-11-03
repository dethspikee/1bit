import sys
import io

from PySide2 import QtCore, QtWidgets, QtGui
from PIL import Image
from converter import convert


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
        self.preview_btn.clicked.connect(self.preview)
        self.convert_btn = QtWidgets.QPushButton('Convert')

        # Disable those buttons at start
        self.preview_btn.setDisabled(True)
        self.convert_btn.setDisabled(True)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.label, 0, 0)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.preview_btn)
        button_layout.addWidget(self.convert_btn)

        layout.addLayout(button_layout, 1, 0)
        window.setLayout(layout)

        self.setCentralWidget(window)

    @QtCore.Slot()
    def preview(self):
        self.preview_btn.setDisabled(True)
        img = Image.open(self.filename)
        img_converted = img.resize((128, 64)).convert('1', dither=Image.NONE)
        bytes_img = io.BytesIO()
        img_converted.save(bytes_img, format=img.format)
        qimg = QtGui.QImage()
        qimg.loadFromData(bytes_img.getvalue())
        pixmap = QtGui.QPixmap(qimg)
        self.label.setPixmap(pixmap)
        self.status.showMessage(f'Previewing {self.filename} as 1-bit bitmap')


    @QtCore.Slot()
    def open_file_dialog(self):
        self.filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open Image', '.', 'Image Files (*.png *.jpg *.jpeg *.bmp)'
        )

        pixmap = QtGui.QPixmap(self.filename)
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
