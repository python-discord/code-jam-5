import os
import sys
import traceback

from PyQt5 import QtCore, QtWidgets

import GUI


class ExceptionHandler:
    def __init__(self):
        pass

    def handler(self, exctype, value, tb, exc=[]):
        exc.extend(traceback.format_exception(exctype, value, tb))
        sys.__excepthook__(exctype, value, tb)

        try:
            self.w.close()
        except AttributeError:
            pass
        self.w = GUI.CrashPop(exc)
        self.w.setup()


if __name__ == "__main__":
    sys.excepthook = ExceptionHandler().handler
    QtCore.QCoreApplication.setApplicationName("Temp Plotter")
    QtCore.QCoreApplication.setOrganizationName("Right Rebels")
    path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppConfigLocation)
    # create org and app folders if not found
    if not os.path.isdir(path):
        if not os.path.isdir(path[:path.rfind("/")]):
            os.mkdir(path[:path.rfind("/")])
        os.mkdir(path)
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    settings = QtCore.QSettings(path + "/config.ini", QtCore.QSettings.IniFormat)
    u = GUI.MainWindow(settings)
    u.setup_ui()
    sys.exit(app.exec_())
