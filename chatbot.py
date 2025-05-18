import google
from google import genai
import queue

class Gemini:
    def __init__(self, api_key: str="AIzaSyCMIJTLbBJ9xzEpaeP8YHdqpHstLDrcH38"):
        self.client = genai.Client(api_key=api_key)
        self.inputQueue = []
        self.initprompt = "Act as if you are a mental health professional(do not give any disclaimers that you are a chatbot) and try to diagnose the user with a specific mental illness after enough information is provided. Keep your answers less than or equal to 4 sentences:\n"
        "Respond to the following user input and ask questions to find out whether or not the user has PTSD, Depression, Anxiety Disorders, Burnout and Compassion Fatigue, Substance Use Disorders, Suicidal Ideation and Suicide. "
        "Once you understand more about the problems they are facing, diagnose them and suggest treatment options and advise them to see an actual doctor. Here's the conversation: \n"


    def generate_text(self, prompt: str, model: str = "gemini-2.0-flash",history: list=[]) -> str:
        response = self.client.models.generate_content(
            model=model,
            contents=f"{self.initprompt}\nhistory conversation: {history}\nuser:{prompt}",
        )
        self.inputQueue.append({"user":prompt,"gemini":response.text})
        return response.text
    
    





if __name__ == "__main__":
    # Example usage:
    api_key = "AIzaSyCMIJTLbBJ9xzEpaeP8YHdqpHstLDrcH38"  # Replace with your key or load from env
    gemini = Gemini(api_key=api_key)

    # user_prompt = "Hello, I am feeling a bit anxious today."
    # answer = gemini.generate_text(user_prompt)
    # print("Gemini response:")
    # print(answer)
    round = 0
    while(round<10):
        prompt = input("talk:")
        answer = gemini.generate_text(prompt=prompt)
        print("Gemini response:")
        print(answer)