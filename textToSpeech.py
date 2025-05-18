# sk_a52a3f251f764099b0e6aadd664150de81630069dad93ec6
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import os

class TextToSpeech:
    def __init__(self):
        load_dotenv()
        self.client = ElevenLabs(
            api_key='sk_a52a3f251f764099b0e6aadd664150de81630069dad93ec6',
            )
    
    def speak(self, text: str):
        audio = self.client.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        play(audio)


if __name__ == "__main__":
    tts = TextToSpeech()
    tts.speak("Hello, I am a text to speech system.")
    

