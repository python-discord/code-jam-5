from PyQt5 import QtWidgets, QtCore, QtGui


class AlbumButton(QtWidgets.QFrame):
    
    selected = QtCore.pyqtSignal(str)

    def __init__(self, image, audio):
        super().__init__()
        self.audio = audio
        self.background_image = QtGui.QPixmap(image).scaled(100, 100, QtCore.Qt.KeepAspectRatioByExpanding)
        self.background_label = QtWidgets.QLabel(self)
        self.background_label.setFixedSize(100, 100)
        self.background_label.setPixmap(self.background_image)
        self.setFixedSize(100, 100)
        self.setCursor(QtCore.Qt.PointingHandCursor)

    def mouseReleaseEvent(self, event):
        """Detect click event, which is when the mouse is released and still hovering over the item."""
        mouse = self.mapToParent(event.pos())
        if self.pos().x() < mouse.x() < self.pos().x() + self.width():
            if self.pos().y() < mouse.y() < self.pos().y() + self.height():
                self.selected.emit(self.audio)
