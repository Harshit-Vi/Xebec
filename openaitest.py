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

