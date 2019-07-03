import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib import cm

import plot


class MainWindow(QtWidgets.QMainWindow):
    stop_plot_signal = QtCore.pyqtSignal()

    def __init__(self, settings):
        super(MainWindow, self).__init__()
        self.central_widget = QtWidgets.QWidget(self)
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.image_label = QtWidgets.QLabel(self.central_widget)
        self.status_bar = QtWidgets.QStatusBar(self)
        self.horizontalSlider = QtWidgets.QSlider(self.central_widget,
                                                  orientation=QtCore.Qt.Horizontal)
        self.bottom_layout = QtWidgets.QHBoxLayout()

        self.move_year_left_button = QtWidgets.QPushButton()
        self.move_year_right_button = QtWidgets.QPushButton()

        self.button_layout = QtWidgets.QVBoxLayout()

        self.plot_button = QtWidgets.QPushButton()
        self.stop_button = QtWidgets.QPushButton(enabled=False)

        self.sdate_animate_layout = QtWidgets.QVBoxLayout()
        self.start_date_layout = QtWidgets.QHBoxLayout()
        self.animate_layout = QtWidgets.QHBoxLayout()

        self.animate_button = QtWidgets.QPushButton(enabled=False)
        self.start_year = QtWidgets.QSpinBox()
        self.start_month = QtWidgets.QComboBox()

        self.end_date_align_layout = QtWidgets.QVBoxLayout()
        self.end_date_layout = QtWidgets.QHBoxLayout()

        self.end_year = QtWidgets.QSpinBox()
        self.end_month = QtWidgets.QComboBox()
        self.preferences_button = QtWidgets.QPushButton()

        self.animate_timer = QtCore.QTimer()
        self.image_count = 0
        self.settings = settings

    def setup_ui(self):
        self.save_default_settings()
        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setCentralWidget(self.central_widget)

        self.setStatusBar(self.status_bar)
        self.status_bar.setSizeGripEnabled(False)

        self.retranslate_ui()
        self.set_ranges_values()
        self.connect_signals()
        self.set_shortcuts()

        spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Expanding,
                                       QtWidgets.QSizePolicy.Expanding)

        self.start_date_layout.addWidget(self.start_month)
        self.start_date_layout.addWidget(self.start_year)

        self.animate_layout.addWidget(self.animate_button)

        self.sdate_animate_layout.addLayout(self.start_date_layout)
        self.sdate_animate_layout.addLayout(self.animate_layout)

        self.button_layout.addWidget(self.plot_button, alignment=QtCore.Qt.AlignCenter)
        self.button_layout.addWidget(self.stop_button, alignment=QtCore.Qt.AlignCenter)

        self.end_date_layout.addWidget(self.end_month)
        self.end_date_layout.addWidget(self.end_year)

        self.end_date_align_layout.addLayout(self.end_date_layout)
        self.end_date_align_layout.addWidget(self.preferences_button)

        self.bottom_layout.addLayout(self.sdate_animate_layout)
        self.bottom_layout.addSpacerItem(spacer)
        self.bottom_layout.addWidget(self.move_year_left_button)
        self.bottom_layout.addLayout(self.button_layout)
        self.bottom_layout.addWidget(self.move_year_right_button)
        self.bottom_layout.addSpacerItem(spacer)
        self.bottom_layout.addLayout(self.end_date_align_layout)

        self.main_layout.addWidget(self.image_label, alignment=QtCore.Qt.AlignCenter)
        self.main_layout.addSpacerItem(spacer)
        self.main_layout.addWidget(self.horizontalSlider)
        self.main_layout.addLayout(self.bottom_layout)

        self.show()
        self.preferences_button.pressed.connect(self.show_options)
        self.set_sizes()

    def set_shortcuts(self):
        year_move_right = QtWidgets.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Right), self)

        year_move_right.activated.connect(lambda: self.horizontalSlider.setValue(
            self.horizontalSlider.value() + int(12 / self.plot_step)))

        year_move_left = QtWidgets.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Left), self)

        year_move_left.activated.connect(lambda: self.horizontalSlider.setValue(
            self.horizontalSlider.value() - int(12 / self.plot_step)))

        month_move_right = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right), self)
        month_move_right.activated.connect(lambda: self.horizontalSlider.setValue(
            self.horizontalSlider.value() + 1))

        month_move_left = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Left), self)
        month_move_left.activated.connect(lambda: self.horizontalSlider.setValue(
            self.horizontalSlider.value() - 1))

    def set_sizes(self):
        self.setFixedSize(850, 650)
        self.image_label.setFixedSize(QtCore.QSize(796, 552))

        font = QtGui.QFont()
        self.move_year_left_button.setFixedWidth(
            QtGui.QFontMetrics(font).boundingRect(self.move_year_left_button.text()).width() + 5)
        self.move_year_right_button.setFixedWidth(
            QtGui.QFontMetrics(font).boundingRect(self.move_year_right_button.text()).width() + 5)

        self.move_year_left_button.setFixedHeight(self.move_year_left_button.width())
        self.move_year_right_button.setFixedHeight(self.move_year_right_button.width())

    def set_ranges_values(self):
        months = ("January", "February", "March", "April", "May", "June", "July",
                  "August", "September", "October", "November", "December")

        self.start_month.addItems(months)
        self.end_month.addItems(months)

        self.horizontalSlider.setRange(-1, -1)
        self.horizontalSlider.setValue(-1)

        self.start_year.setRange(1850, 2010)
        self.end_year.setRange(1980, 2019)
        self.start_year.setValue(1980)
        self.end_year.setValue(2010)

    def connect_signals(self):
        self.horizontalSlider.valueChanged.connect(self.change_image)

        # ensure only valid dates can be entered
        self.start_month.currentIndexChanged.connect(self.date_changed)
        self.end_year.valueChanged.connect(self.date_changed)
        self.start_year.valueChanged.connect(self.date_changed)

        self.animate_button.pressed.connect(self.animate)
        self.plot_button.pressed.connect(self.plot)
        self.stop_button.pressed.connect(self.quit_current_tasks)

        self.move_year_left_button.pressed.connect(lambda: self.horizontalSlider.setValue(
            self.horizontalSlider.value() - int(12 / self.plot_step)))
        self.move_year_right_button.pressed.connect(lambda: self.horizontalSlider.setValue(
            self.horizontalSlider.value() + int(12 / self.plot_step)))

    def retranslate_ui(self):
        self.setWindowTitle("Plotstats")
        self.plot_button.setText("Plot")
        self.stop_button.setText("Stop")
        self.animate_button.setText("Play")
        self.preferences_button.setText("Preferences")
        self.move_year_right_button.setText("-->")
        self.move_year_left_button.setText("<--")
        self.move_year_left_button.setToolTip("Skip year")
        self.move_year_right_button.setToolTip("Skip year")

    def show_options(self):
        self.preferences_button.setEnabled(False)
        w = SettingsPop(self.settings, self)
        w.setup_ui()
        w.settings_signal.connect(self.refresh_settings)
        w.close_signal.connect(lambda: self.preferences_button.setEnabled(True))

    def save_default_settings(self):
        if not self.settings.value("Plot step"):
            self.settings.setValue("Playback FPS", 5)
            self.settings.setValue("Plot step", 1)
            self.settings.setValue("Color map", "seismic")
            self.settings.sync()

        self.plot_step = self.settings.value("Plot step", type=int)
        self.play_fps = self.settings.value("Playback FPS", type=int)
        self.color_map = self.settings.value("Color map")

    def refresh_settings(self, values):
        self.play_fps = int(values[0])
        self.plot_step = int(values[1])
        self.color_map = values[2]

    def set_status(self, message):
        self.status_bar.showMessage(message)

    def plot(self):
        self.image_count = 0
        QtGui.QPixmapCache.clear()
        self.stop_button.setEnabled(True)
        self.plot_button.setEnabled(False)
        self.animate_button.setEnabled(False)

        # send dates in decimal format to worker
        start_date = self.start_year.value() + (1 + self.start_month.currentIndex() * 2) / 24
        end_date = self.end_year.value() + (1 + self.end_month.currentIndex() * 2) / 24
        self.worker = plot.Plotter(start_date, end_date, self.plot_step, self.color_map, self)
        self.worker.image_increment_signal.connect(self.add_image)
        self.worker.finished.connect(self.del_worker)
        self.worker.status_signal.connect(self.set_status)

        self.worker.start()

    def del_worker(self):
        self.worker.quit()
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
        self.animate_button.setEnabled(False)
        self.animate_timer.timeout.connect(self.animation)
        self.animate_timer.start(int(1000 / self.play_fps))

    def animation(self):
        self.horizontalSlider.setValue(self.horizontalSlider.value() + 1)
        if self.horizontalSlider.value() == self.horizontalSlider.maximum():
            self.stop_timer()
            self.stop_button.setEnabled(False)

    def stop_timer(self):
        self.animate_timer.stop()
        try:
            self.animate_timer.timeout.disconnect()
        except TypeError:
            pass
        self.animate_button.setEnabled(True)

    def quit_current_tasks(self):
        self.stop_plot_signal.emit()
        self.stop_timer()
        self.stop_button.setEnabled(False)

    def closeEvent(self, *args, **kwargs):
        super(QtWidgets.QMainWindow, self).closeEvent(*args, **kwargs)
        try:
            self.worker.clear_plots()
        except AttributeError:
            pass


class SettingsPop(QtWidgets.QDialog):
    settings_signal = QtCore.pyqtSignal(tuple)
    close_signal = QtCore.pyqtSignal()

    def __init__(self, settings, parent=None):
        super(SettingsPop, self).__init__(parent)
        self.main_layout = QtWidgets.QVBoxLayout()

        self.fps_layout = QtWidgets.QHBoxLayout()
        self.fps_label = QtWidgets.QLabel()
        self.fps_spin = QtWidgets.QSpinBox()

        self.step_layout = QtWidgets.QHBoxLayout()
        self.step_label = QtWidgets.QLabel()
        self.step_combo = QtWidgets.QComboBox()

        self.color_map_layout = QtWidgets.QHBoxLayout()
        self.color_map = QtWidgets.QPushButton()
        self.color_map_label = QtWidgets.QLabel()

        self.settings = settings

        self.save_button = QtWidgets.QPushButton()

    def setup_ui(self):
        spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.MinimumExpanding,
                                       QtWidgets.QSizePolicy.MinimumExpanding)
        self.setLayout(self.main_layout)

        self.fps_layout.addWidget(self.fps_label)
        self.fps_layout.addSpacerItem(spacer)
        self.fps_spin.setRange(1, 60)
        self.fps_spin.setAccelerated(True)
        self.fps_layout.addWidget(self.fps_spin)
        self.main_layout.addLayout(self.fps_layout)

        self.step_layout.addWidget(self.step_label)
        self.step_combo.addItems(("1", "3", "6", "12", "24"))
        self.step_layout.addSpacerItem(spacer)
        self.step_layout.addWidget(self.step_combo)
        self.main_layout.addLayout(self.step_layout)

        self.color_map_layout.addWidget(self.color_map)
        self.color_map_layout.addWidget(self.color_map_label, alignment=QtCore.Qt.AlignRight)

        self.main_layout.addLayout(self.color_map_layout)
        self.main_layout.addSpacerItem(spacer)
        self.main_layout.addWidget(self.save_button, alignment=QtCore.Qt.AlignCenter)

        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.color_map.pressed.connect(self.color_map_chooser)
        self.save_button.pressed.connect(self.save_settings)

        self.retranslate_ui()
        self.grab_settings()
        self.show()

    def retranslate_ui(self):
        self.fps_label.setText("Playback speed [FPS]")
        self.step_label.setText("Step of plotter")
        self.color_map.setText("Choose color map")
        self.save_button.setText("Save preferences")

    def grab_settings(self):
        self.fps_spin.setValue(self.settings.value("Playback FPS", type=int))
        step_value = self.settings.value("Plot step")
        self.step_combo.setCurrentIndex(("1", "3", "6", "12", "24").index(step_value))
        self.color_map_label.setText(self.settings.value("Color map"))

    def save_settings(self):
        settings = (self.fps_spin.value(), self.step_combo.currentText(),
                    self.color_map_label.text())
        self.settings.setValue("Playback FPS", settings[0])
        self.settings.setValue("Plot step", settings[1])
        self.settings.setValue("Color map", settings[2])
        self.settings.sync()
        self.settings_signal.emit(settings)
        self.close()

    def color_map_chooser(self):
        w = ColorMapChooser(self.cursor().pos(), self)
        w.setup_ui()
        w.choice_signal.connect(self.set_label)

    def set_label(self, text):
        self.color_map_label.setText(text)

    def closeEvent(self, *args, **kwargs):
        super(QtWidgets.QDialog, self).closeEvent(*args, **kwargs)
        self.close_signal.emit()


class ColorMapChooser(QtWidgets.QDialog):
    choice_signal = QtCore.pyqtSignal(str)

    def __init__(self, pos, parent=None):
        super(ColorMapChooser, self).__init__(parent)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.color_list = QtWidgets.QListWidget()
        self.start_pos = pos

    def setup_ui(self):
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.move(self.start_pos)
        self.main_layout.addWidget(self.color_list)
        self.setLayout(self.main_layout)
        self.color_list.addItems(cm.cmap_d.keys())

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint, True)
        self.setWindowFlags(QtCore.Qt.Popup)

        self.color_list.itemDoubleClicked.connect(self.send_choice)
        self.show()

    def send_choice(self, item):
        self.choice_signal.emit(item.text())


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
