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

        ## Widgets
        # Labels and text edits
        self.label = QtWidgets.QLabel(parent=self)
        self.label_for_slider = QtWidgets.QLabel(parent=self)
        self.label_for_slider.setText('Threshold: 0')
        self.textedit = QtWidgets.QTextEdit()
        self.threshold_check = QtWidgets.QCheckBox(parent=self, text='Apply threshold')

        self.label.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored
        )

        # Buttons
        self.preview_btn = QtWidgets.QPushButton('Preview')
        self.preview_btn.clicked.connect(self.preview)
        self.convert_btn = QtWidgets.QPushButton('Convert')
        self.convert_btn.clicked.connect(self.get_bytes)
        # Disable those buttons at start
        self.preview_btn.setDisabled(True)
        self.convert_btn.setDisabled(True)

        # Black / White Threshold Slider
        self.slider = QtWidgets.QSlider(
            parent=self, orientation=QtCore.Qt.Horizontal
        )
        self.slider.sliderMoved.connect(self.get_slider_value)
        self.slider.valueChanged.connect(self.get_slider_value)
        self.slider.setMinimum(0)
        self.slider.setMaximum(255)

        # Layout
        window = QtWidgets.QWidget()

        layout_skeleton = QtWidgets.QVBoxLayout()

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.label, stretch=1)
        top_layout.addWidget(self.textedit, stretch=1)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.preview_btn)
        button_layout.addWidget(self.convert_btn)

        threshold_layout = QtWidgets.QHBoxLayout()
        threshold_layout.addWidget(self.threshold_check)
        threshold_layout.addWidget(self.slider)
        threshold_layout.addWidget(self.label_for_slider)

        layout_skeleton.addLayout(top_layout)
        layout_skeleton.addLayout(threshold_layout)
        layout_skeleton.addLayout(button_layout)

        window.setLayout(layout_skeleton)
        self.setCentralWidget(window)

    @QtCore.Slot()
    def get_slider_value(self):
        value = self.slider.value()
        self.label_for_slider.setText(f'Threshold: {value}')
        return value

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
        threshold_value = self.get_slider_value()
        threshold_set = self.threshold_check.isChecked()
        try:
            pixmap = resize(self.filename, threshold_value, threshold_set)
            self.label.setPixmap(pixmap)
        except Exception as e:
            self.status.showMessage(f'{e}')
        else:
            self.status.showMessage(
                f'Previewing {self.filename} as 1-bit bitmap'
            )

    @QtCore.Slot()
    def open_file_dialog(self):
        self.filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open Image', '.', 'Image Files (*.png *.jpg *.jpeg *.bmp)'
        )

        self.textedit.clear()

        pixmap = QtGui.QPixmap(self.filename)
        pixmap_w, pixmap_h = pixmap.size().width(), pixmap.size().height()
        if not (
            pixmap_w < self.computedWidth and pixmap_h < self.computedHeight
        ):
            pixmap = pixmap.scaled(
                self.computedWidth,
                self.computedHeight,
                QtCore.Qt.KeepAspectRatio,
            )
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
