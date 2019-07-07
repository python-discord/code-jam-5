def run():
    import sys
    from thoughtful_termites.shared import qt
    from .widgets import ControlPanel
    app = qt.QApplication(sys.argv)
    sys.excepthook = sys.__excepthook__

    control_panel = ControlPanel()
    control_panel.show()

    return app.exec()
