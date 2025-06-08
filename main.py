import site
import sys

import language
import speech_recognition as sr
import os
import webbrowser
import pyttsx3   #Text-to-speech library
import wikipedia
import openai
import subprocess, sys


# Initialize text-to-speech engine
engine = pyttsx3.init()

def say(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand(): # to take voice command
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #r.pause_threshold = 1 # To check the audio quality fir machine to recognize
        audio = r.listen(source) #listens the audio

        try: #Try catch to avoid errors
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in") # instead of google, amazon and bing etc. can be used
            print(f"User said: {query}\n") #  for debugging
            return query
        except Exception as e:
            return "Some error occured. I am sorry."

if __name__ == '__main__':
    print('PyCharm')
    say("Hello, I am Xebec")
    say("I've been awakened")

    while True:
        print("Listening.....")
        query = takeCommand()


        # To stop all operation and exit terminal
        if "stop" in query.lower():
            say("Shutting down...")
            sys.exit()  # Terminates program immediately

        sites = [["youtube","https://www.youtube.com"],
                 ["instagram","https://www.instagram.com"],
                 ["facebook","https://www.facebook.com"],
                 ["google","https://www.google.com"],
                 ["Chat Gpt","https://www.chatgpt.com"],
                 ["spotify","https://www.spotify.com"]]

        # Check if any site matches the query
        for site in sites:
            if f"open {site[0]}" in query.lower():
                say(f"Opening {site[0]}...")
                webbrowser.open(site[1])
                break  # Prevent infinite loop

        #Moveing "Open Music" check OUTSIDE the loop otherwise it will need to open site first to trigger it **
        if "play music" in query.lower():
            say("Playing your music now!")
            musicPath = r"C:\Users\Harshit Singh\Downloads\CHOOT VOL. 1 - Yo Yo Honey Singh Ft. Badshah (Official Music Video) - Mafia Mundeer.mp3"

            #Use Windows-specific file opener
            if sys.platform == "win32":
                os.startfile(musicPath)  # Correct way to open files on Windows
    #query