from google import genai
from google.genai import types

from api.utils.env_utils import get_required_env_var

GEMINI_API_KEY = get_required_env_var("GEMINI_API_KEY")

gemini_client = genai.Client(api_key=GEMINI_API_KEY)


def generate_content_with_gemini(
    prompt: str,
) -> str:
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0),
    )
    if not response.text:
        raise ValueError("No text returned from Gemini API")
    return response.text
