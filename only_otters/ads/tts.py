import tempfile
from gtts import gTTS


# https://stackoverflow.com/questions/27749105/play-video-in-qt-from-byte-stream
def as_callack_audio(text):

    audio = gTTS(text, lang='en')

    tfile = tempfile.NamedTemporaryFile(delete=False)
    audio.write_to_fp(tfile)
    path = tfile.name
    tfile.close()

    return tfile.name
