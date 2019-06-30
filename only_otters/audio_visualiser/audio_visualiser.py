from PyQt5 import QtWidgets, QtGui, QtCore
from .fft_analyser import FFTAnalyser
import numpy as np


class AudioVisualiser(QtWidgets.QWidget):
    """Shows a visual representation of audio from a QMediaPlayer"""

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.setFixedSize(200, 200)
        self.max_radius = min(self.width(), self.height())//2
        self.min_radius = self.max_radius / 2
        self.fill_colour = QtCore.Qt.black
        self.pen_colour = QtCore.Qt.black
        self.amps = np.array([])
        self.start_visualising()

    def amp_polygon(self):
        """
        Uses polar co-ordinate formulae in order to plot a
        circular polygon based off of amplitudes
        """
        polygon = QtGui.QPolygonF()
        for theta, amp in zip(np.linspace(-np.pi / 2, np.pi * 1.5, self.amps.size), self.amps):
            r = self.min_radius + (self.max_radius - self.min_radius) * amp

            # When wanting to obtain a cartesian point (x, y) at r distance from the origin
            # and theta distance rotated away from the positive x axis, you can use these formulae
            # x = rcos(theta)
            # y = rsin(theta)

            x = r * np.cos(theta)
            y = r * np.sin(theta)
            polygon.append(QtCore.QPointF(x, y))

        # Centering the polygon
        polygon.translate(self.width()//2, self.height()//2)
        return polygon

    def set_amplitudes(self, amps):
        """Sets the amplitudes for the visualiser and plots them"""
        self.amps = np.array(amps)
        self.repaint()

    def start_visualising(self):
        """Begins the visualiser thread"""
        self.analyser_thread = FFTAnalyser(self.player)
        self.analyser_thread.calculated_visual.connect(self.set_amplitudes)
        self.analyser_thread.start()

    def paintEvent(self, event):
        """Plots the amplitudes"""
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen_colour)
        painter.setBrush(self.fill_colour)

        polygon = self.amp_polygon()
        painter.drawPolygon(polygon)
