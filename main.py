import sys                        # Provides access to system-specific parameters and functions
import speech_recognition as sr   # Enables speech recognition functionality
import pyttsx3                    # Text-to-speech conversion for voice output
import datetime                   # Handles date and time functions
import webbrowser                 # Allows opening web pages in a browser
import os                         # Facilitates interaction with the operating system
import openai

# text-to-speech engine
engine = pyttsx3.init()

#OpenAI API Key
open.api_key = os.getenv("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")

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
            print(f"User said: {query}")  # Debugging print statement
            return query.lower()
        except Exception as e:
            print("Error recognizing voice:", e)  # Debugging error print statement
            return ""

def ask_chatgpy(prompt):
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
    )
    answer = response['choices'][0]['message']['content']
    

def run_Xebec():
    say("Hello, I am Xebec")
    say("I've been awakened")

    while True:
        query = takeCommand()

        if "stop" in query:
            say("Shutting down...")
            return "stop"  # Signal to stop the assistant

        # todo: add feature to play specific song
        elif "play music" in query:
            say("Playing your music now!")
            musicPath = r"C:\Users\Harshit Singh\Downloads\CHOOT VOL. 1 - Yo Yo Honey Singh Ft. Badshah (Official Music Video) - Mafia Mundeer.mp3"
            os.startfile(musicPath)

        elif "the time" in query:
            strfTime = datetime.datetime.now().strftime('%I:%M %p')
            say(f"The time is {strfTime}")

        # todo: add more sites.
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

# **Main Loop to stop Assistant When Needed**
while True:
    status = run_Xebec()

    if status == "stop":
        say("Going offline...")
        break # exits the main loop
        


