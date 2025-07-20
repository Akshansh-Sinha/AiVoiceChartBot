import tempfile
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os

def speak(text, lang='hi'):
    # Create a temp file path (don't open it yet!)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        path = tmp.name

    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(path)  # Save MP3 after file is closed
        audio = AudioSegment.from_mp3(path)
        play(audio)
    finally:
        os.remove(path)  # Clean up temp file
