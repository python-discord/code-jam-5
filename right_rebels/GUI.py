import sys

from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.central_widget = QtWidgets.QWidget(self)
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.image_label = QtWidgets.QLabel(self.central_widget)
        self.status_bar = QtWidgets.QStatusBar(self)
        self.horizontalSlider = QtWidgets.QSlider(self.central_widget)
        self.year_label = QtWidgets.QLabel(self.central_widget)
        self.date_range_layout = QtWidgets.QHBoxLayout()
        self.plot_button = QtWidgets.QPushButton()
        self.start_year = QtWidgets.QSpinBox()
        self.end_year = QtWidgets.QSpinBox()
        self.start_month = QtWidgets.QComboBox()
        self.end_month = QtWidgets.QComboBox()

    def setup_ui(self):
        self.resize(800, 600)
        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setCentralWidget(self.central_widget)
        self.setStatusBar(self.status_bar)
        self.status_bar.setSizeGripEnabled(False)

        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setRange(00, 10)
        self.horizontalSlider.valueChanged.connect(self.change_image)

        self.change_image(0)

        months = ("January", "February", "March", "April", "May", "June", "July",
                  "August", "September", "October", "November", "December")

        self.start_month.addItems(months)
        self.end_month.addItems(months)

        self.start_month.setMaximumWidth(85)
        self.end_month.setMaximumWidth(85)
        self.start_year.setMaximumWidth(50)
        self.end_year.setMaximumWidth(50)

        self.start_year.setRange(1880, 2018)
        self.end_year.setRange(1880, 2018)
        self.start_year.setValue(1980)
        self.end_year.setValue(2010)
        self.start_year.setAccelerated(True)
        self.end_year.setAccelerated(True)

        spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Expanding,
                                       QtWidgets.QSizePolicy.Expanding)

        self.date_range_layout.addWidget(self.start_month, alignment=QtCore.Qt.AlignLeft)
        self.date_range_layout.addWidget(self.start_year, alignment=QtCore.Qt.AlignLeft)
        self.date_range_layout.addSpacerItem(spacer)
        self.date_range_layout.addWidget(self.plot_button)
        self.date_range_layout.addSpacerItem(spacer)

        self.date_range_layout.addWidget(self.end_month)
        self.date_range_layout.addWidget(self.end_year)

        self.main_layout.addWidget(self.image_label, alignment=QtCore.Qt.AlignCenter)
        self.main_layout.addSpacerItem(spacer)
        self.main_layout.addWidget(self.horizontalSlider)
        self.main_layout.addWidget(self.year_label, alignment=QtCore.Qt.AlignCenter)
        self.main_layout.addLayout(self.date_range_layout)
        self.main_layout.addSpacerItem(spacer)

        self.retranslate_ui()
        self.show()

    def retranslate_ui(self):
        self.setWindowTitle("Plotstats")

    def change_image(self, index):
        pixmap = QtGui.QPixmap(f"plots/image{index}")
        self.image_label.setPixmap(pixmap)
        self.year_label.setText(str(index))
        self.setFixedSize(pixmap.width(), pixmap.height())


class CrashPop(QtWidgets.QDialog):
    def __init__(self, tb):
        super(CrashPop, self).__init__()
        self.label = QtWidgets.QLabel()
        self.text_browser = QtWidgets.QTextBrowser()
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.traceback = tb

    def setup(self):
        self.setFixedSize(400, 250)
        self.setWindowTitle("Error")

        self.label.setText("An unexpected error has occured")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)

        for line in self.traceback:
            self.text_browser.append(line)

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.text_browser)
        self.setLayout(self.main_layout)

        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.setModal(True)

        self.show()

    def closeEvent(self, *args, **kwargs):
        super(QtWidgets.QDialog, self).closeEvent(*args, **kwargs)
        sys.exit(-1)
