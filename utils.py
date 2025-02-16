from gtts import gTTS
import os
from pydub import AudioSegment

def generate_speech(text, filename):
    base_path = os.path.join(os.getcwd(), "assets")
    mp3_path = os.path.join(base_path, "mp3")
    wav_path = os.path.join(base_path, "wav")
    # Generate speech
    tts = gTTS(text, lang="en")
    mp3_filepath = os.path.join(mp3_path, filename + ".mp3")
    tts.save(mp3_filepath)

    # Convert to WAV
    audio = AudioSegment.from_mp3(mp3_filepath)
    wav_filepath = os.path.join(wav_path, filename + ".wav")
    audio.export(os.path.join(os.getcwd(), "assets", "wav", wav_filepath), format="wav")

    print(f"Audio saved as {filename}.wav and {filename}.mp3")
