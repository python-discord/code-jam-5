import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets

import plot


class MainWindow(QtWidgets.QMainWindow):
    stop_plot_signal = QtCore.pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.central_widget = QtWidgets.QWidget(self)
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.image_label = QtWidgets.QLabel(self.central_widget)
        self.status_bar = QtWidgets.QStatusBar(self)
        self.horizontalSlider = QtWidgets.QSlider(self.central_widget)
        self.year_label = QtWidgets.QLabel(self.central_widget)
        self.date_range_layout = QtWidgets.QHBoxLayout()

        self.button_layout = QtWidgets.QVBoxLayout()

        self.plot_button = QtWidgets.QPushButton()
        self.stop_button = QtWidgets.QPushButton(enabled=False)

        self.sdate_animate_layout = QtWidgets.QVBoxLayout()
        self.start_date_layout = QtWidgets.QHBoxLayout()
        self.animate_layout = QtWidgets.QHBoxLayout()

        self.animate_button = QtWidgets.QPushButton(enabled=False)
        self.animate_fps = QtWidgets.QSpinBox()
        self.start_year = QtWidgets.QSpinBox()
        self.start_month = QtWidgets.QComboBox()

        self.end_year = QtWidgets.QSpinBox()
        self.end_month = QtWidgets.QComboBox()

        self.animate_timer = QtCore.QTimer()
        self.image_count = 0

    def setup_ui(self):
        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(830, 675)
        self.setCentralWidget(self.central_widget)
        self.setStatusBar(self.status_bar)
        self.status_bar.setSizeGripEnabled(False)

        self.image_label.setFixedSize(QtCore.QSize(796, 552))

        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setRange(-1, 0)
        self.horizontalSlider.setValue(-1)
        self.horizontalSlider.valueChanged.connect(self.change_image)

        months = ("January", "February", "March", "April", "May", "June", "July",
                  "August", "September", "October", "November", "December")

        self.start_month.addItems(months)
        self.end_month.addItems(months)

        self.start_month.setMaximumWidth(85)
        self.end_month.setMaximumWidth(85)

        # ensure only valid dates can be entered
        self.start_month.currentIndexChanged.connect(self.date_changed)
        self.end_year.valueChanged.connect(self.date_changed)
        self.start_year.valueChanged.connect(self.date_changed)

        self.start_year.setMaximumWidth(50)
        self.end_year.setMaximumWidth(50)

        self.start_year.setRange(1850, 2010)
        self.end_year.setRange(1980, 2019)
        self.start_year.setValue(1980)
        self.end_year.setValue(2010)

        self.animate_fps.setRange(1, 60)
        self.animate_button.setFixedWidth(81)

        self.animate_button.pressed.connect(self.animate)
        self.plot_button.pressed.connect(self.plot)
        self.stop_button.pressed.connect(self.quit_current_tasks)

        spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Expanding,
                                       QtWidgets.QSizePolicy.Expanding)

        self.start_date_layout.addWidget(self.start_month)
        self.start_date_layout.addWidget(self.start_year)

        self.animate_layout.addWidget(self.animate_button)
        self.animate_layout.addWidget(self.animate_fps)

        self.sdate_animate_layout.addLayout(self.start_date_layout)
        self.sdate_animate_layout.addLayout(self.animate_layout)

        self.date_range_layout.addLayout(self.sdate_animate_layout)
        self.date_range_layout.addSpacerItem(spacer)

        self.button_layout.addWidget(self.plot_button)
        self.button_layout.addWidget(self.stop_button)

        self.date_range_layout.addLayout(self.button_layout)
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
        self.plot_button.setText("Plot")
        self.stop_button.setText("Stop")
        self.animate_button.setText("Play")

    def set_status(self, message):
        self.status_bar.showMessage(message)

    def plot(self):
        self.image_count = 0
        self.stop_button.setEnabled(True)
        self.plot_button.setEnabled(False)
        self.animate_button.setEnabled(False)
        # send dates in decimal format to worker
        start_date = self.start_year.value() + (1 + self.start_month.currentIndex() * 2) / 24
        end_date = self.end_year.value() + (1 + self.end_month.currentIndex() * 2) / 24
        self.worker = plot.Plotter(start_date, end_date, self)

        self.worker.image_increment_signal.connect(self.add_image)
        self.worker.finished.connect(self.del_worker)
        self.worker.status_signal.connect(self.set_status)

        self.worker.start()

    def del_worker(self):
        self.worker.quit()
        del self.worker
        self.stop_button.setEnabled(False)
        self.plot_button.setEnabled(True)
        self.animate_button.setEnabled(True)

    def add_image(self):
        self.horizontalSlider.setRange(0, self.image_count)

        if self.horizontalSlider.value() == self.horizontalSlider.maximum() - 1:
            self.horizontalSlider.setValue(self.image_count)

        self.image_count += 1

    def change_image(self, index):
        pixmap = QtGui.QPixmap(f"plots/plot{index}")
        self.image_label.setPixmap(pixmap)

    def date_changed(self):
        for item_index in range(0, 12):
            self.start_month.model().item(item_index).setEnabled(True)
            self.end_month.model().item(item_index).setEnabled(True)

        if self.start_year.value() == self.end_year.value():
            for item_index in range(0, self.start_month.currentIndex()):
                self.end_month.model().item(item_index).setEnabled(False)
            if self.end_month.currentIndex() < self.start_month.currentIndex():
                self.end_month.setCurrentIndex(self.start_month.currentIndex())

        if self.start_year.value() == 2019:
            for item_index in range(5, 12):
                self.start_month.model().item(item_index).setEnabled(False)
            if self.start_month.currentIndex() > 4:
                self.start_month.setCurrentIndex(4)

        if self.end_year.value() == 2019:
            for item_index in range(5, 12):
                self.end_month.model().item(item_index).setEnabled(False)
            if self.end_month.currentIndex() > 4:
                self.end_month.setCurrentIndex(4)

        self.start_year.setRange(1850, self.end_year.value())
        self.end_year.setRange(self.start_year.value(), 2019)

    def animate(self):
        self.horizontalSlider.setValue(0)
        self.stop_button.setEnabled(True)
        if self.animate_timer.isActive():
            self.animate_timer.stop()
            self.animate_timer.timeout.disconnect()
        self.animate_timer.timeout.connect(self.animation)
        self.start_time = time.time()
        self.animate_timer.start(int(1000 / self.animate_fps.value()))

    def animation(self):
        if self.horizontalSlider.value() == self.horizontalSlider.maximum():
            self.animate_timer.stop()
            self.animate_timer.timeout.disconnect()
            self.stop_button.setEnabled(False)
        else:
            self.horizontalSlider.setValue(self.horizontalSlider.value() + 1)

    def quit_current_tasks(self):
        self.stop_plot_signal.emit()
        self.animate_timer.stop()
        self.stop_button.setEnabled(False)

    def closeEvent(self, *args, **kwargs):
        super(QtWidgets.QMainWindow, self).closeEvent(*args, **kwargs)
        plot.Plotter(None, None).clear_plots()


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
