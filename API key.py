import openai

# Set your API key here
openai.api_key = "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"  # Replace with your actual key

try:
    models = openai.Model.list()
    print("✅ Available models for your API key:\n")
    for model in models["data"]:
        print(model["id"])
except Exception as e:
    print(f"❌ Error: {e}")
