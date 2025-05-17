import os
import threading
import queue
import speech_recognition as sr
from pydub import AudioSegment

# Optional: Set ffmpeg path if using mp3 (not needed for microphone)
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

class LiveSpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio_queue = queue.Queue()
        self.text_queue = queue.Queue(maxsize=10)
        self.stop_event = threading.Event()

    def listen_loop(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("[Listener] Listening started...")

            while not self.stop_event.is_set():
                try:
                    audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=None)
                    self.audio_queue.put(audio)
                except Exception as e:
                    print(f"[Listener] Error: {e}")

    def process_loop(self):
        print("[Processor] Waiting for audio...")
        while not self.stop_event.is_set() or not self.audio_queue.empty():
            try:
                audio = self.audio_queue.get(timeout=1)
                text = self.recognizer.recognize_google(audio)
                self.text_queue.put(text, block=False)
                print("[Transcript]", text)
            except queue.Empty:
                continue
            except sr.UnknownValueError:
                print("[Transcript] [Could not understand speech]")
            except sr.RequestError as e:
                print(f"[Transcript] [API error: {e}]")
    def getSentencce(self):
        return self.text_queue.get()
    
    def hasSentence(self):
        return not self.text_queue.empty()
    
    def start(self):
        self.listener_thread = threading.Thread(target=self.listen_loop)
        self.processor_thread = threading.Thread(target=self.process_loop)

        self.listener_thread.start()
        self.processor_thread.start()

    def stop(self):
        self.stop_event.set()
        self.listener_thread.join()
        self.processor_thread.join()
        print("[System] Stopped cleanly.")

if __name__ == "__main__":
    stt = LiveSpeechToText()
    try:
        stt.start()
        input("\nPress ENTER to stop...\n")
    finally:
        stt.stop()
