# std
import time
import os

# qt
from PyQt5 import QtCore

# other
from pydub import AudioSegment
import numpy as np


class FFTAnalyser(QtCore.QThread):
    """Analyses a song on a playlist using FFTs."""

    calculated_visual = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, player: 'MusicPlayer'):  # noqa: F821
        super().__init__()
        self.player = player
        self.reset_media()
        self.player.currentMediaChanged.connect(self.reset_media)

        self.resolution = 40

    def reset_media(self):
        """Resets the media to the currently playing song."""
        audio_file = self.player.currentMedia().canonicalUrl().path()
        if os.name == 'nt' and audio_file.startswith('/'):
            audio_file = audio_file[1:]
        if audio_file:
            try:
                self.song = AudioSegment.from_file(audio_file).set_channels(1)
            except PermissionError:
                self.start_animate = False
            else:
                self.samples = np.array(self.song.get_array_of_samples())

                self.max_sample = self.samples.max()
                self.maximum_amp = self.max_sample // 4
                self.points = np.zeros(self.resolution)
                self.start_animate = True
        else:
            self.start_animate = False

    def calculate_amps(self):
        """Calculates the amplitudes used for visualising the media."""

        sample_count = int(self.song.frame_rate * 0.05)
        start_index = int((self.player.position()/1000) * self.song.frame_rate)
        v_sample = self.samples[start_index:start_index+sample_count]  # samples to analyse

        # use FFTs to analyse frequency and amplitudes
        fourier = np.fft.fft(v_sample)
        freq = np.fft.fftfreq(fourier.size, d=0.05)
        amps = 2/v_sample.size * np.abs(fourier)
        data = np.array([freq, amps]).T

        point_range = 1 / self.resolution
        point_samples = []

        if not data.size:
            return

        for f in np.arange(0, 1, point_range):
            # get the amps which are in between the frequency range
            amps = data[(f - point_range < data[:, 0]) & (data[:, 0] < f)]
            if not amps.size:
                point_samples.append(0)
            else:
                point_samples.append(amps.max())

        # Add the point_samples to the self.points array, the reason we have a separate
        # array (self.bars) is so that we can fade out the previous amplitudes from
        # the past
        for n, amp in enumerate(point_samples):
            amp *= 2.5  # amplify the amplitude :)

            if (self.points[n] > 0 and amp < self.points[n] or
                    self.player.state() in (self.player.PausedState, self.player.StoppedState)):
                self.points[n] -= self.points[n] / 2  # fade out
            else:
                self.points[n] = min(amp, self.maximum_amp)

            if self.points[n] < 1:
                self.points[n] = 0

        # Mirror the amplitudes, these are renamed to 'rs' because we are using them
        # for polar plotting, which is plotted in terms of r and theta
        rs = np.concatenate((self.points, np.flip(self.points)))

        # the fade area represents the area in which the points are faded to 0 to create a smooth
        # transition between the mirrors, in this case it is 1/12th of the total area
        fade_area = int(np.ceil(rs.size * 1/12))

        # the fade is calculated using an exponential graph of 2^x, as to create a smooth curve
        fade_out = np.array([rs[0] / 2**x for x in range(fade_area)])
        fade_in = np.flip(fade_out)

        rs = np.concatenate((fade_in, rs, fade_out))

        # they are divided by the highest sample in the song to normalise the
        # amps in terms of decimals from 0 -> 1
        self.calculated_visual.emit(rs / self.max_sample)

    def run(self):
        """Runs the animate function depending on the song."""
        while True:
            if self.start_animate:
                try:
                    self.calculate_amps()
                except ValueError:
                    self.calculated_visual.emit(np.zeros(self.resolution))
                    self.start_animate = False
            time.sleep(0.025)
