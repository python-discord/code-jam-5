# Temp plotter
# Copyright (C) 2019  Right Rebels
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
