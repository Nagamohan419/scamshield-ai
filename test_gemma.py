
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)

print("Connecting to Gemma 4...")

response = client.models.generate_content(
    model="gemma-4-26b-a4b-it",
    contents="What are three warning signs of a scam SMS?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="minimal"
        )
    )
)

print("\nGemma 4 response:\n")
print(response.text)
