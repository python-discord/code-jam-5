import tempfile
from gtts import gTTS


# https://stackoverflow.com/questions/27749105/play-video-in-qt-from-byte-stream
def as_callack_audio(text: str) -> str:
    """Perform Text-To-Speech on input text, then saves to a file and return filepath."""

    audio = gTTS(text, lang='en')

    tfile = tempfile.NamedTemporaryFile(delete=False)
    audio.write_to_fp(tfile)
    tfile.close()

    return tfile.name
