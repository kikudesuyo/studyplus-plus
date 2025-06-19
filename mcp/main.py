import asyncio

from fastmcp import Client
from google import genai
from google.genai import types

from api.utils.env_utils import get_required_env_var

GEMINI_API_KEY = get_required_env_var("GEMINI_API_KEY")

mcp_client = Client("./mcp/server.py")
gemini_client = genai.Client(api_key=GEMINI_API_KEY)


async def main():
    async with mcp_client:
        response = await gemini_client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents="Roll 3 dice!",
            config=types.GenerateContentConfig(
                temperature=0,
                tools=[mcp_client.session],  # Pass the FastMCP client session
            ),
        )
        print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
