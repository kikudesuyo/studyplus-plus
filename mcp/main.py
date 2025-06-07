import asyncio

from fastmcp import Client
from google import genai

# client = genai.Client(api_key="AIzaSyDHIfE1DFylXt2xB9rfV80jZHOMQo_N3VY")
# export GEMINI_API_KEY="AIzaSyDHIfE1DFylXt2xB9rfV80jZHOMQo_N3VY"

mcp_client = Client("./mcp/server.py")
gemini_client = genai.Client()


async def main():
    async with mcp_client:
        response = await gemini_client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents="Roll 3 dice!",
            config=genai.types.GenerateContentConfig(
                temperature=0,
                tools=[mcp_client.session],  # Pass the FastMCP client session
            ),
        )
        print(response.text)


if __name__ == "__main__":
    asyncio.run(main())


# client = genai.Client(api_key="AIzaSyDHIfE1DFylXt2xB9rfV80jZHOMQo_N3VY")

# response = client.models.generate_content(
#     model="gemini-2.0-flash", contents="Explain how AI works in a few words"
# )
# print(response.text)
