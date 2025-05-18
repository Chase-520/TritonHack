import google
from google import genai

class Gemini:
    def __init__(self, api_key: str="AIzaSyCMIJTLbBJ9xzEpaeP8YHdqpHstLDrcH38"):
        self.client = genai.Client(api_key=api_key)

    def generate_text(self, prompt: str, model: str = "gemini-2.0-flash") -> str:
        response = self.client.models.generate_content(
            model=model,
            contents=f"Role play as a mental health doctor, respond to the following user input, 2 sentences max: {prompt}",
        )
        return response.text


if __name__ == "__main__":
    # Example usage:
    api_key = "AIzaSyCMIJTLbBJ9xzEpaeP8YHdqpHstLDrcH38"  # Replace with your key or load from env
    gemini = Gemini(api_key=api_key)

    user_prompt = "Hello, I am feeling a bit anxious today. I want to kill myself"
    answer = gemini.generate_text(user_prompt)
    print("Gemini response:")
    print(answer)
