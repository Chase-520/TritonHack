import sys
from pydub import AudioSegment

def main():
    if len(sys.argv) < 2:
        print("No audio file path provided", file=sys.stderr)
        sys.exit(1)

    audio_path = sys.argv[1]

    try:
        audio = AudioSegment.from_file(audio_path)
        duration_sec = len(audio) / 1000.0
        print(f"Audio duration: {duration_sec:.2f} seconds")
    except Exception as e:
        print(f"Error processing audio: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
