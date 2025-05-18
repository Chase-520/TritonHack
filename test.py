import asyncio
import os
import pyaudio
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
DEEPGRAM_API_KEY = "73b8b9646f15c71d594cf57ffbd85d0532712a12"

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
TIMEOUT_SECONDS = 30

async def transcribe_audio():
    if not DEEPGRAM_API_KEY:
        raise ValueError("DEEPGRAM_API_KEY is not set in the environment")

    # Initialize Deepgram client
    deepgram = DeepgramClient(DEEPGRAM_API_KEY)

    # Create websocket connection to Deepgram live transcription
    dg_connection = deepgram.listen.websocket.v("1")

    # Define callback to print transcriptions
    def on_message(self, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if transcript.strip():
            print(f"Transcript: {transcript}")

    def on_open(self, open, **kwargs):
        print("Connection opened")

    def on_error(self, error, **kwargs):
        print(f"Error: {error}")

    # Register callbacks
    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
    dg_connection.on(LiveTranscriptionEvents.Open, on_open)
    dg_connection.on(LiveTranscriptionEvents.Error, on_error)

    # Configure transcription options
    options = LiveOptions(
        model="nova-3",
        language="en",
        smart_format=True,
        encoding="linear16",
        channels=1,
        sample_rate=RATE
    )

    # Start the websocket connection
    dg_connection.start(options)

    # Setup PyAudio to read from mic
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Listening... Speak into your microphone.")

    try:
        async def stream_audio():
            while True:
                data = stream.read(CHUNK, exception_on_overflow=False)
                dg_connection.send(data)
                await asyncio.sleep(0.01)

        # Run audio streaming for TIMEOUT_SECONDS seconds
        await asyncio.wait_for(stream_audio(), timeout=TIMEOUT_SECONDS)

    except asyncio.TimeoutError:
        print("\nTimeout reached, stopping...")
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        dg_connection.finish()
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    asyncio.run(transcribe_audio())
