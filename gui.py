"""
Not used due to high latency and lack of multi-threading
"""
import tkinter as tk
from PIL import Image, ImageTk
import sounddevice as sd
from scipy.io.wavfile import write
import threading
import numpy as np
from speechToText import LiveSpeechToText
from textToSpeech import TextToSpeech
from chatbot import Gemini
import time

class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Voice Assistant")
        self.root.geometry("600x400")

        # App state
        self.recording = False
        self.fs = 44100
        self.audio_data = []
        self.history = []

        # Components
        self.converter = LiveSpeechToText()
        self.speaker = TextToSpeech()
        self.bot = Gemini()

        # Load and resize background image (use new Pillow API)
        self.bg_image = Image.open("bgF.png")
        self.bg_image = self.bg_image.resize((600, 400), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Setup Canvas with background image
        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        self.canvas.bg_photo = self.bg_photo  # Keep reference to prevent GC

        # UI Elements
        self.start_button = tk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.stop_button = tk.Button(self.root, text="Stop Recording", command=self.stop_recording)
        self.context_label = tk.Label(self.root, text=" ", wraplength=500, justify="left", bg="white")

        # Place UI elements on canvas
        self.canvas.create_window(200, 250, window=self.start_button)
        self.canvas.create_window(400, 250, window=self.stop_button)
        self.canvas.create_window(300, 330, window=self.context_label)

    def record_audio(self):
        self.audio_data = []

        def callback(indata, frames, time, status):
            if self.recording:
                self.audio_data.append(indata.copy())

        with sd.InputStream(callback=callback, channels=1, samplerate=self.fs):
            while self.recording:
                sd.sleep(100)

        # Once recording stops, process audio on the main thread via .after

    def start_recording(self):
        if self.recording:
            return  # Already recording
        self.recording = True
        threading.Thread(target=self.record_audio, daemon=True).start()

    def stop_recording(self):
        if not self.recording:
            return
        self.recording = False
        time.sleep(0.5)  # Give some time for the audio buffer to clear
        self.process_audio()

    def process_audio(self):
        if not self.audio_data:
            return

        final_audio = np.concatenate(self.audio_data, axis=0)
        int_audio = np.int16(final_audio * 32767)
        write("recorded_audio.wav", self.fs, int_audio)

        duration = len(final_audio) / self.fs
        print(f"Recorded Duration: {duration:.2f} seconds")

        try:
            transcript = self.converter.transcribe_file("recorded_audio.wav")
        except Exception as e:
            transcript = f"[Error] {e}"

        if transcript == "[Could not understand speech]":
            self.speaker.speak("I am sorry, I didn't hear you, could you repeat that?")
        else:
            response = self.bot.generate_text(transcript, history=self.history)
            self.context_label.config(text=f"Transcript:\n{transcript}\n\nResponse:\n{response}")
            time.sleep(1)
            self.speaker.speak(response)
            self.history.append({"user": transcript, "bot": response})


if __name__ == "__main__":
    import sys
    import traceback

    def custom_excepthook(exc_type, exc_value, exc_traceback):
        print("Uncaught exception:")
        traceback.print_exception(exc_type, exc_value, exc_traceback)

    sys.excepthook = custom_excepthook

    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
