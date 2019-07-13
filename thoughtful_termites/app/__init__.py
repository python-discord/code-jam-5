def run():
    """
    Convenience function for running the app.
    """
    import sys
    from thoughtful_termites.shared import qt
    from thoughtful_termites.app.widgets import GoalListWindow

    app = qt.QApplication(sys.argv)
    sys.excepthook = sys.__excepthook__

    window = GoalListWindow()
    window.show()

    return app.exec()
