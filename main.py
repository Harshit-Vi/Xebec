import speech_recognition as sr
import os
import pyttsx3   #Text-to-speech library

# Initialize text-to-speech engine
engine = pyttsx3.init()

def say(text):
    engine.say(text)
    engine.runAndWait()

if __name__ == '__main__':
    print('PyCharm')
    say("Hello, I am Xebec")