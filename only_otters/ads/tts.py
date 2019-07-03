from gtts import gTTS
from io import BytesIO
from PyQt5.QtCore import QByteArray, QBuffer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import tempfile

from contextlib import contextmanager
import io


def as_audio_tp(text):

    audio = gTTS(text, lang='en')
    t =  tempfile.NamedTemporaryFile()
    audio.write_to_fp(t)

    print(t.name)

    print(t.closed)
    return t.name, t


if __name__ == "__main__":

    text = """
    Fact n°38: Climate change is a hoac. Dony says so, so it must be true.
    """    

    with as_audio_stream(text) as audio_buffer:

        player = QMediaPlayer()
        player.setMedia(QMediaContent(), audio_buffer)

        player.play()

# https://stackoverflow.com/questions/27749105/play-video-in-qt-from-byte-stream