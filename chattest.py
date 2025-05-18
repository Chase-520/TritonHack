import sounddevice as sd
import numpy as np
import tempfile
import wave
import threading
import queue
import time
from faster_whisper import WhisperModel

# Load Whisper model (use "tiny" for faster performance)
model = WhisperModel("tiny", compute_type="int8")  # "base", "small", etc. also available

# Audio recording settings
samplerate = 16000  # Whisper expects 16kHz input
channels = 1
chunk_duration = 2  # Seconds
audio_queue = queue.Queue()

def record_audio():
    """Record audio from microphone and add to queue."""
    print("[System] Starting microphone...")
    while True:
        recording = sd.rec(int(chunk_duration * samplerate), samplerate=samplerate,
                           channels=channels, dtype='int16')
        sd.wait()
        audio_queue.put(recording.copy())

def transcribe_loop():
    """Transcribe audio chunks using faster-whisper."""
    print("[System] Starting transcription loop...")
    while True:
        print("[System] Listening...")
        chunk = audio_queue.get()

        # Save debug audio (optional, comment out if not needed)
        with wave.open("debug.wav", 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # 16-bit PCM
            wf.setframerate(samplerate)
            wf.writeframes(chunk.tobytes())
        print("[Debug] Saved chunk to debug.wav")

        # Save to temp file and transcribe
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as f:
            with wave.open(f.name, 'wb') as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(2)
                wf.setframerate(samplerate)
                wf.writeframes(chunk.tobytes())

            segments, _ = model.transcribe(f.name, beam_size=5)

            found = False
            for segment in segments:
                found = True
                print("[Transcript]", segment.text)

            if not found:
                print("[Transcript] [No speech detected]")

if __name__ == "__main__":
    # Run threads for recording and transcription
    threading.Thread(target=record_audio, daemon=True).start()
    threading.Thread(target=transcribe_loop, daemon=True).start()

    print("Press Ctrl+C to stop...\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[System] Exiting...")
