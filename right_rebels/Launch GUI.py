import sys
import traceback

from PyQt5 import QtWidgets

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
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    u = GUI.MainWindow()
    u.setup_ui()
    sys.exit(app.exec_())
