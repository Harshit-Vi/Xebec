import pyttsx3

engine = pyttsx3.init('sapi5')

def list_voices():
    voices = engine.getProperty('voices')
    for i, voice in enumerate(voices):
        print(f"{i + 1}. {voice.name}")
        engine.setProperty('voice', voice.id)
        engine.say(f"This is {voice.name}")
    engine.runAndWait()

list_voices()
