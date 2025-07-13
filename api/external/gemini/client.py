# from google import genai
from google.genai import Client, types

from api.utils.env_utils import get_required_env_var


class GeminiClient(Client):
    def __init__(self):
        GEMINI_API_KEY = get_required_env_var("GEMINI_API_KEY")
        super().__init__(api_key=GEMINI_API_KEY)

    def generate_content(
        self,
        prompt: str,
    ) -> str:
        response = self.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0),
        )
        if not response.text:
            raise ValueError("No text returned from Gemini API")
        return response.text
