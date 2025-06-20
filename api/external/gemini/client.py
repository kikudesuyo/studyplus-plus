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


if __name__ == "__main__":
    prompt = """
    あなたはプロの漫才師です。以下のエピソードが100点満点で何点かを評価してください。点数だけを出力してください。
    イヤホンを1時間くらい探していたら、イヤホンをしていた。
    """
    result = generate_content_with_gemini(prompt)
    print(f"Gemini response: {result}")
