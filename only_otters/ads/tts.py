from gtts import gTTS


def as_audio_stream(text):
    # TODO: Stream byte data to QMediaPlayer w/o using a file
    audio = gTTS(text)
    raise NotImplementedError