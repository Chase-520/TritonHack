import google
from google import genai

class Gemini:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def generate_text(self, prompt: str, model: str = "gemini-2.0-flash") -> str:
        response = self.client.models.generate_content(
            model=model,
            contents=prompt,
        )
        return response.text


if __name__ == "__main__":
    # Example usage:
    api_key = "AIzaSyCMIJTLbBJ9xzEpaeP8YHdqpHstLDrcH38"  # Replace with your key or load from env
    gemini = Gemini(api_key=api_key)

    user_prompt = "Talk like an anime girl in japanese"
    answer = gemini.generate_text(user_prompt)
    print("Gemini response:")
    print(answer)
