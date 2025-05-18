import tkinter as tk
import sounddevice as sd
from scipy.io.wavfile import write
import threading
import numpy as np
import time
from speechToText import LiveSpeechToText  # <- Replace with your actual import
from textToSpeech import TextToSpeech  # <- Replace with your actual import
from chatbot import Gemini  # <- Replace with your actual import
# Globals
recording = False
fs = 44100  # Sample rate
audio_data = []
converter = LiveSpeechToText()
speaker = TextToSpeech()
bot  = Gemini()
history = []
def record_audio():
    global recording, audio_data
    audio_data = []

    def callback(indata, frames, time, status):
        if recording:
            audio_data.append(indata.copy())

    with sd.InputStream(callback=callback, channels=1, samplerate=fs):
        while recording:
            sd.sleep(100)

    # After stopping, process audio
    process_audio()

def start_recording():
    global recording
    recording = True
    status_label.config(text="Recording...")
    threading.Thread(target=record_audio).start()

def stop_recording():
    global recording
    recording = False
    status_label.config(text="Stopped and processing...")

def process_audio():
    if not audio_data:
        status_label.config(text="No audio data recorded.")
        return

    final_audio = np.concatenate(audio_data, axis=0)

    # Convert float32 [-1, 1] to int16 PCM
    int_audio = np.int16(final_audio * 32767)
    write("recorded_audio.wav", fs, int_audio)
    print("Audio saved to 'recorded_audio.wav'")

    duration = len(final_audio) / fs
    print(f"Recorded Duration: {duration:.2f} seconds")

    # Speech-to-text
    try:
        transcript = converter.transcribe_file("recorded_audio.wav")
    except Exception as e:
        transcript = f"[Error] {e}"
    response = bot.generate_text(transcript,history=history)
    status_label.config(text=f"Saved! Duration: {duration:.2f} sec")
    contextlabel.config(text=f"Transcript:\n{transcript}\nResponse:\n{response}")
    speaker.speak(response)
    history.append({"user": transcript, "bot":response})

    


# === Tkinter UI ===
root = tk.Tk()
root.title("Mic Recorder")

tk.Button(root, text="Start Recording", command=start_recording).pack(pady=10)
tk.Button(root, text="Stop Recording", command=stop_recording).pack(pady=10)
contextlabel = tk.Label(root, text="text")
contextlabel.pack(pady=5)
status_label = tk.Label(root, text="Ready")
status_label.pack(pady=5)

root.mainloop()
