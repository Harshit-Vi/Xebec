import openai
import os
openai.api_key = os.getenv("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")

def ask_chatgpt(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}],
            max_tokens=200,
            temperature=0.7
        )
        answer = response['choices'][0]['message']['content']
        return answer.strip()
    except Exception as e:
        return f"Error: {e}"
openai.api_key = os.getenv("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")

def ask_chatgpt(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}],
            max_tokens=200,
            temperature=0.7
        )
        answer = response['choices'][0]['message']['content']
        return answer.strip()
    except Exception as e:
        return f"Error: {e}"

