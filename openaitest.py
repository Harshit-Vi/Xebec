import os
import openai
from config import apikey
print(apikey)
exit()
openai.api_key = apikey

# Make sure your OpenAI API key is set in the environment variables
openai.api_key = os.getenv("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")

response = openai.ChatCompletion.create(
  model="gpt-4",  # or "gpt-3.5-turbo"
  messages=[
    {"role": "user", "content": "write a letter for resignation to boss"}
  ],
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response['choices'][0]['message']['content'])
