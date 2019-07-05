def run():
    import sys
    from thoughtful_termites.app import qt
    from thoughtful_termites.app.widgets import GoalListWindow

    app = qt.QApplication(sys.argv)

    window = GoalListWindow()
    window.show()

    return app.exec()
