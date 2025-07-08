from together import Together
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

if not api_key:
    print("❌ TOGETHER_API_KEY is not set.")
    exit(1)

# Create client with key
client = Together(api_key=api_key)

# Try valid chat completion
try:
    response = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",  # Use any valid Together model
        messages=[{"role": "user", "content": "Hello, are you working?"}],
        max_tokens=50
    )
    print("✅ API is working! Response:")
    print(response.choices[0].message.content.strip())

except Exception as e:
    print("❌ API key is invalid or request failed:")
    print(e)
