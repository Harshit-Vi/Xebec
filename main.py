import site
import sys
import language
import speech_recognition as sr
import os
import webbrowser
import pyttsx3   #Text-to-speech library
import wikipedia
import openai
import subprocess, sys # used for external command and managing paths
import datetime # For date time query


# Initialize text-to-speech engine
engine = pyttsx3.init()

def say(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand(): # to take voice command
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #r.pause_threshold = 1 # To check the audio quality for machine to recognize
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


# To start and stop all operation and exit terminal
def run_Xebec():
    while True:
        query = takeCommand()

        if "stop" in query.lower():
            say("Shutting down...")
            break # exits the loop

        elif "start" in query.lower():
            say("System coming online...")
            return # exit function and restart main loop

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
        # to ask time
        if "the time" in query.lower():
            strfTime = datetime.datetime.now().strftime('%I:%M %p')
            say(f"the time is {strfTime}")

# Start xebec again when asked
while True:
    command= takeCommand()

    if "start" in command:
        run_Xebec()

    elif "stop" in command:
        say("Going offline...")
        sys.exit
    #query