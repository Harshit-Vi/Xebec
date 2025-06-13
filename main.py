import sys                        # Provides access to system-specific parameters and functions
import speech_recognition as sr   # Enables speech recognition functionality
import pyttsx3                    # Text-to-speech conversion for voice output
import datetime                   # Handles date and time functions
import webbrowser                 # Allows opening web pages in a browser
import os                         # Facilitates interaction with the operating system
from together import Together     # Official Together SDK

# text-to-speech engine
engine = pyttsx3.init()

# Initialize Together client (direct key or from environment)
together_api_key = "tgp_v1_RSVq1hWYbQbyGMussZ57xgLB5yZ_ArpuaHW-TnG36Hk"
client = Together(api_key=together_api_key)

def say(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except Exception as e:
            print("Error recognizing voice:", e)
            return ""

def ask_me(prompt):
    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",  # Or use any other Together-supported model
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Together SDK error: {e}"

def run_Xebec():
    say("Hello, I am Xebec")
    say("I've been awakened")

    while True:
        query = takeCommand()

        if "stop" in query:
            say("Shutting down...")
            return "stop"

        elif "play music" in query:
            say("Playing your music now!")
            musicPath = r"C:\Users\Harshit Singh\Downloads\CHOOT VOL. 1 - Yo Yo Honey Singh Ft. Badshah (Official Music Video) - Mafia Mundeer.mp3"
            os.startfile(musicPath)

        elif "the time" in query:
            strfTime = datetime.datetime.now().strftime('%I:%M %p')
            say(f"The time is {strfTime}")

        elif "open" in query:
            sites = {
                "youtube": "https://www.youtube.com",
                "instagram": "https://www.instagram.com",
                "facebook": "https://www.facebook.com",
                "google": "https://www.google.com",
                "chat gpt": "https://www.chatgpt.com",
                "spotify": "https://www.spotify.com"
            }

            for site in sites:
                if f"open {site}" in query:
                    say(f"Opening {site}...")
                    webbrowser.open(sites[site])
                    break

        elif any(x in query for x in ["who is ", "what is", "tell me about", "define", "ask me"]):
            answer = ask_me(query)
            print("ChatGpt:", answer)
            say(answer)

# Main loop to run Xebec
while True:
    status = run_Xebec()
    if status == "stop":
        say("Going offline...")
        break

