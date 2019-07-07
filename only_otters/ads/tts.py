# std
import tempfile

# other
from gtts import gTTS


# https://stackoverflow.com/questions/27749105/play-video-in-qt-from-byte-stream
def text_to_audio(text: str) -> str:
    """Perform Text-To-Speech on input text, then saves to a file and return filepath."""

    audio = gTTS(text, lang='en')

    with tempfile.NamedTemporaryFile(delete=False) as tfile:
        audio.write_to_fp(tfile)

    return tfile.name
