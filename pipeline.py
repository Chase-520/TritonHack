import speech_recognition as sr
import openai
from gtts import gTTS
import os
from playsound import playsound
import tempfile

# STEP 1: Audio Input → Text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Speak something...")
        audio = recognizer.listen(source)
        print("⌛ Recognizing...")
        try:
            text = recognizer.recognize_google(audio)
            print(f"📝 You said: {text}")
            return text
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
            return ""
        except sr.RequestError:
            print("❌ Speech service unavailable.")
            return ""

# STEP 2: Send Text to OpenAI ChatGPT API
def get_gpt_response(prompt, api_key):
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use free-tier eligible model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        reply = response['choices'][0]['message']['content'].strip()
        print(f"🤖 GPT says: {reply}")
        return reply
    except Exception as e:
        print(f"❌ Error with OpenAI API: {e}")
        return "Sorry, I couldn't process that."

# STEP 3: Text to Speech → Audio Output
def speak_text(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
        tts.save(fp.name)
        playsound(fp.name)

# MAIN WORKFLOW
if __name__ == "__main__":
    API_KEY = "your-openai-api-key-here"  # Replace with your OpenAI API key

    input_text = speech_to_text()
    if input_text:
        response = get_gpt_response(input_text, API_KEY)
        speak_text(response)
