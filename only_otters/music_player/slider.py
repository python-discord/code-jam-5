from PyQt5.QtWidgets import QSlider


class Slider(QSlider):

    def __init__(self, progress_bar):
        super().__init__(progress_bar)

    def mousePressEvent(self, event):
        print('mpe:', event)