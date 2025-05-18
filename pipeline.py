"""
A test pipeline for chatbot feedback loop. No ai used
"""
from speechToText import LiveSpeechToText
from chatbot import Gemini
from textToSpeech import TextToSpeech


class Pipeline:
    def __init__(self):
        self.listener = LiveSpeechToText()
        self.chatbot = Gemini()
        self.talker = TextToSpeech()

    def start_listening(self):
        self.listener.start()

    def run(self):
        self.start_listening()
        while True:
            if self.listener.hasSentence():
                sentence = self.listener.getSentencce()
                print(f"[Pipeline] Received: {sentence}")
                response = self.chatbot.generate_text(sentence)
                print(f"[Pipeline] Response: {response}")
                self.talker.speak(response)

    def start(self):
        self.run()

if __name__ == "__main__":
    pipeline = Pipeline()
    try:
        pipeline.start()
    except KeyboardInterrupt:
        print("\n[Pipeline] Stopped by user.")
        pipeline.listener.stop()