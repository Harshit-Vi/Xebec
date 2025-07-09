# At the top with other initializations
global client
client = Together(api_key=together_api_key)

def ask_me(prompt):
    try:
        response = client.chat.completions.create(  # Now recognizes client
            model="deepseek-ai/DeepSeek-V3",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"