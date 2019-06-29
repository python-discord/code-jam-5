import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Only Otters"
        self.createUI()

    def createUI(self):
        menubar = self.menuBar()
        self.setWindowTitle(self.title)
        self.setGeometry(250, 250, 250, 200)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MusicPlayer()
    sys.exit(app.exec_())
    
