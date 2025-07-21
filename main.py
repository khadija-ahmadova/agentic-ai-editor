import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("API key not found")
        return 1

    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("Prompt not provided\nUsage: python script.py <prompt>")
        return 1
    
    user_prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", contents=messages,
        )
    except Exception as e:
        print(f"API error: {e}")
        return 1
    
    print(response.text)

    if len(sys.argv) == 3:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    sys.exit(main())
