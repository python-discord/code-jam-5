from PyQt5 import QtWidgets, QtCore

# https://www.qtcentre.org/threads/31570-A-progress-bar-that-has-a-slider-on-top-of-it
# https://doc.qt.io/qt-5/stylesheet-examples.html

from .slider import Slider


class Seeker(QtWidgets.QProgressBar):

    timestamp_updated = QtCore.pyqtSignal(str)

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.player.positionChanged.connect(self.update_position)
        self.setTextVisible(False)
        self.setRange(0, 1000)
        self.setFixedHeight(5)

        self.setStyleSheet(
            """
            QProgressBar {
                border: 0px solid #555;
                border-radius: 2px;
                background-color: #666;
            }

            QProgressBar::chunk {
                background-color: white;
                width: 1px;
            }
            """
        )

        self.slider = Slider(self)
        # Bind slider slots to 


    def update_position(self, milliseconds):
        if self.player.duration():
            self.setValue((milliseconds/self.player.duration())*self.maximum())
            duration = int(milliseconds / 1000)
            seconds = str(duration % 60)
            minutes = str(duration // 60)
            self.timestamp_updated.emit(minutes.zfill(2) + ':' + seconds.zfill(2))
            
            # Set slider position
            pass

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
