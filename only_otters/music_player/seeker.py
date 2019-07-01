from PyQt5 import QtWidgets


class Seeker(QtWidgets.QProgressBar):

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.player.positionChanged.connect(self.update_position)
        self.setTextVisible(False)
        self.setRange(0, 1000)
        self.setFixedHeight(10)

    def update_position(self, milliseconds):
        if self.player.duration():
            self.setValue((milliseconds/self.player.duration())*self.maximum())

    def mousePressEvent(self, event):
        self.dragging = True
        value = (event.x() / self.width()) * self.maximum()
        self.player.setPosition((event.x() / self.width()) * self.player.duration())
        self.setValue(value)

    def mouseMoveEvent(self, event):
        if self.dragging:
            value = (event.x() / self.width()) * self.maximum()
            self.player.setPosition((event.x() / self.width()) * self.player.duration())
            self.setValue(value)

    def mouseReleaseEvent(self, event):
        self.dragging = False
