from speechToText import LiveSpeechToText
from chatbot import Gemini


class Pipeline:
    def __init__(self):
        self.listener = LiveSpeechToText()
        self.chatbot = Gemini()

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

    def start(self):
        self.run()

if __name__ == "__main__":
    pipeline = Pipeline()
    try:
        pipeline.start()
    except KeyboardInterrupt:
        print("\n[Pipeline] Stopped by user.")
        pipeline.listener.stop()