import os
import tempfile
import speech_recognition as sr
from pydub import AudioSegment

# Manually specify ffmpeg and ffprobe locations
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def mp3_to_wav(self, mp3_path: str, duration_sec: int = None) -> str:
        audio = AudioSegment.from_mp3(mp3_path)
        if duration_sec:
            audio = audio[:duration_sec * 1000]
        temp_wav_path = tempfile.mktemp(suffix=".wav")
        audio.export(temp_wav_path, format="wav")
        return temp_wav_path

    def transcribe(self, audio_path: str, duration_sec: int = 15) -> str:
        wav_path = self.mp3_to_wav(audio_path, duration_sec)
        try:
            with sr.AudioFile(wav_path) as source:
                audio_data = self.recognizer.record(source)
                return self.recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return "[Unrecognized speech]"
        except sr.RequestError as e:
            return f"[API error: {e}]"
        finally:
            os.remove(wav_path)

    def live_transcribe(self, timeout: int = 5, phrase_time_limit: int = 5):
        """
        Live speech-to-text from the microphone.
        timeout: how long to wait for phrase start (seconds)
        phrase_time_limit: max seconds to listen per phrase
        """
        with sr.Microphone() as source:
            print("Adjusting for ambient noise, please wait...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Ready to transcribe. Speak now!")

            try:
                audio_data = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                print("Processing audio...")
                text = self.recognizer.recognize_google(audio_data)
                return text
            except sr.WaitTimeoutError:
                return "[No speech detected - timeout]"
            except sr.UnknownValueError:
                return "[Could not understand speech]"
            except sr.RequestError as e:
                return f"[API error: {e}]"

if __name__ == "__main__":
    stt = SpeechToText()

    # Offline file transcription example
    mp3_path = r"C:\Users\TEMP.AD.000\Downloads\President John F. Kennedy's _Peace Speech_.mp3"
    result = stt.transcribe(mp3_path, duration_sec=15)
    print("Transcription (First 15 seconds):")
    print(result)

    # Live microphone transcription example
    print("\nNow starting live transcription from microphone...")
    live_result = stt.live_transcribe(timeout=5, phrase_time_limit=7)
    print("Live Transcription:")
    print(live_result)
