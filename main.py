import site

import language
import speech_recognition as sr
import os
import webbrowser
import pyttsx3   #Text-to-speech library

# Initialize text-to-speech engine
engine = pyttsx3.init()

def say(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand(): # to take voice command
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1 # To check the audio quality fir machine to recognize
        audio = r.listen(source) #listens the audio

        try: #Try catch to avoid errors
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
        sites = [["youtube","https://www.youtube.com"], ["instagram","https://www.instagram.com"],
                 ["google","https://www.google.com"],["Chat Gpt","https://www.chatgpt.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]}...")
                webbrowser.open(site[1])
                break # to prevent infinite looping
        #say(query)