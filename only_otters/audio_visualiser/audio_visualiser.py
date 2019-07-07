from PyQt5 import QtWidgets, QtGui, QtCore
from .fft_analyser import FFTAnalyser
from pathlib import Path
import numpy as np


class AudioVisualiser(QtWidgets.QWidget):
    """Shows a visual representation of audio from a QMediaPlayer."""

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.setFixedSize(200, 200)
        self.max_radius = min(self.width(), self.height())//2
        self.min_radius = self.max_radius / 2.5
        self.fill_colour = QtCore.Qt.black
        self.pen_colour = QtCore.Qt.black
        self.red_flames()
        self.amps = np.array([])
        self._draw_center_piece()
        self._start_visualising()

    def _draw_center_piece(self):
        """Draws the center image for the audio visualiser"""
        layout = QtWidgets.QHBoxLayout()

        pixmap = QtGui.QPixmap(str(Path('only_otters/images/earth.png')))
        pixmap = pixmap.scaled(self.min_radius*2+3, self.min_radius*2+3, QtCore.Qt.KeepAspectRatio)
        self.center_piece = QtWidgets.QLabel()
        self.center_piece.setAlignment(QtCore.Qt.AlignCenter)
        self.center_piece.setPixmap(pixmap)
        layout.addWidget(self.center_piece)

        self.setLayout(layout)

    def amp_polygon(self):
        """
        Uses polar co-ordinate formulae in order to plot a
        circular polygon based off of amplitudes.
        """
        # There are three polygons for each colour of the flame
        large_poly = QtGui.QPolygonF()
        medium_poly = QtGui.QPolygonF()
        small_poly = QtGui.QPolygonF()

        for theta, amp in zip(np.linspace(-np.pi / 2, np.pi * 1.5, self.amps.size), self.amps):
            r = self.min_radius + (self.max_radius - self.min_radius) * amp

            # When wanting to obtain a cartesian point (x, y) at r distance from the origin
            # and theta distance rotated away from the positive x axis, you can use these formulae
            # x = rcos(theta)
            # y = rsin(theta)

            x = r * np.cos(theta)
            y = r * np.sin(theta)
            variance = np.random.random()*0.05
            large_poly.append(QtCore.QPointF(x, y))
            medium_poly.append(QtCore.QPointF(x*(0.9+variance), y*(0.9+variance)))
            small_poly.append(QtCore.QPointF(x*(0.8+variance), y*(0.8+variance)))

        # Centering the polygons
        large_poly.translate(self.width()//2, self.height()//2)
        medium_poly.translate(self.width()//2, self.height()//2)
        small_poly.translate(self.width()//2, self.height()//2)

        return large_poly, medium_poly, small_poly

    def set_amplitudes(self, amps):
        """Sets the amplitudes for the visualiser and plots them."""
        self.amps = np.array(amps)
        self.repaint()

    def _start_visualising(self):
        """Begins the visualiser thread."""
        self.analyser_thread = FFTAnalyser(self.player)
        self.analyser_thread.calculated_visual.connect(self.set_amplitudes)
        self.analyser_thread.start()

    def red_flames(self):
        self.flames = [QtCore.Qt.red, QtGui.QColor('#E86100'), QtCore.Qt.yellow]

    def green_flames(self):
        self.flames = [QtGui.QColor('#54ff47'), QtGui.QColor('#4be83f'), QtGui.QColor('#43d638')]

    def paintEvent(self, event):
        """Plots the amplitudes."""
        painter = QtGui.QPainter(self)
        polygon_red, polygon_orange, polygon_yellow = self.amp_polygon()

        painter.setPen(self.flames[0])
        painter.setBrush(self.flames[0])
        painter.drawPolygon(polygon_red)

        painter.setPen(self.flames[1])
        painter.setBrush(self.flames[1])
        painter.drawPolygon(polygon_orange)

        painter.setPen(self.flames[2])
        painter.setBrush(self.flames[2])
        painter.drawPolygon(polygon_yellow)
