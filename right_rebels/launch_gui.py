import os
import sys
import traceback

from PyQt5 import QtCore, QtWidgets

import gui


class ExceptionHandler:
    def __init__(self):
        pass

    def handler(self, exctype, value, tb, exc=None):
        exc = exc or []
        exc.extend(traceback.format_exception(exctype, value, tb))
        sys.__excepthook__(exctype, value, tb)

        # close previous window if multiple exceptions occur
        try:
            self.w.close()
        except AttributeError:
            pass
        self.w = gui.CrashPop(exc)
        self.w.setup()


if __name__ == "__main__":
    # set exception handler for exceptions in qt app event loop
    sys.excepthook = ExceptionHandler().handler
    path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppConfigLocation)
    # create org and app folders if not found
    if not os.path.isdir(path):
        if not os.path.isdir(path[:path.rfind("/")]):
            os.mkdir(path[:path.rfind("/")])
        os.mkdir(path)
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("Right Rebels")
    app.setApplicationName("Temp Plotter")
    app.setStyle("Fusion")
    settings = QtCore.QSettings(path + "/config.ini", QtCore.QSettings.IniFormat)
    ui = gui.MainWindow(settings)
    ui.setup_ui()
    sys.exit(app.exec_())
