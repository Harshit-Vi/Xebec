from docx import Document         # For creation of documents
import sys                        # Provides access to system-specific parameters and functions
import speech_recognition as sr   # Enables speech recognition functionality
import pyttsx3                    # Text-to-speech conversion for voice output
import datetime                   # Handles date and time functions
import webbrowser                 # Allows opening web pages in a browser
import os                         # Facilitates interaction with the operating system
from together import Together     # Official Together SDK
import time                       # Obviously for time lol
import random                     # For random number
import re                         # For removing char that are illegal in a file name
import subprocess                 # Create and manage subprocesses
import difflib                    # Used to match near accurate words ( example : luv for love)


# text-to-speech engine
engine = pyttsx3.init(driverName='sapi5')

# for api functioning and voice recognisation
def say(text):
    engine.say(text)
    engine.runAndWait()


# To see the installed voices
def list_available_voices():
    voices = engine.getProperty('voices')
    for voice in voices:
        print(f"Name: {voice.name}, ID: {voice.id}, Gender: {voice.gender if hasattr(voice, 'gender') else 'unknown'}")

# Initialize Together client (direct key or from environment)
from dotenv import load_dotenv
load_dotenv()

together_api_key = os.getenv("TOGETHER_API_KEY")

if not together_api_key:
    print("Error: TOGETHER_API_KEY is not set in the environment")
    say("I can't start without a valid API key")
    sys.exit(1)

client = Together(api_key=together_api_key)

# voice recognition , Interpretation & voice to text .
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except Exception as e:
            print("Error recognizing voice:", e)
            say("I didn't catch that. please say that again.")
            return ""

# For Voice Change
def set_voice_by_name(name: str):
    name = name.lower().strip()

  # To replace the original voice name
    name_aliases = {
        "jeera": "zira",
        "jeeera": "zira",
        "zira": "zira",
        "david": "david",
    }
    # Replace with corrected name if alias exist
    name = name_aliases.get(name, name)

    voices=engine.getProperty('voices')
    for voice in voices:
        if name in voice.name.lower():
            engine.setProperty('voice', voice.id)
            say(f"Hi, I am {voice.name} here in your service.")
            return

    say("Sorry, I couldn't find that voice.")
    print(f"No ,matching voice for: {name}")

# For creation of documents.
def create_word_doc_from_topic(topic):
    say(f"Generating word document for {topic}")
    content = ask_me(f"Write a detailed article about {topic}")

    try:
        doc =Document()
        doc.add_heading(f"Topic: {topic}", 0)
        doc.add_paragraph(content)

        # ✅ Clean the topic string to make a safe filename
        safe_topic = re.sub(r'[\\/*?:"<>|]', "_", topic)
        filename = f"{safe_topic.replace(' ', '_')}.docx"

        doc.save(filename)

        say(f"Word file created as {filename}")
        print(f"Saved as: {filename}")
    except Exception as e:
        say("Sorry, I couldn't create the document.")
        print(f"Error creating Word document: {e}")

#---number guessing game---
def number_guessing_game():
    say("let's play a number guessing game.")
    number = random.randint(1, 20)
    for i in range (5):
        say("Take a guess.")
        guess = takeCommand()
        if guess.isdigit():
            guess = int(guess)
            if guess < number:
                say("Your guess is too low.")
            elif guess > number:
                say("Your guess is too high.")
            else:
                say("Congratulations, you guessed the number!")
                return
        else:
            say("please say a number.")

    say(f"Sorry! The number I was thinking of was {number}.Better luck next time.")

#--- Truth or Dare Game---
truths = [
    "What is your biggest fear?",
    "What's a secret you've never told anyone?",
    "Have you ever lied to your best friend?",
    "What's the most embarrassing thing you've done?",
    "Who was your first crush?"
]

dares = [
    "Do 10 pushups right now.",
    "Sing the chorus of your favorite song.",
    "Dance like a chicken for 15 seconds.",
    "Text someone 'I like you' and screenshot the response.",
    "Do an impression of your favorite actor."
]

def get_players():
    players = []
    print("Enter player names (type 'done' when finished):")
    while True:
        name = input("Player name: ").strip()
        if name.lower() == 'done':
            break
        elif name:
            players.append(name)
    return players

def play_game(players):
    print("\n🎉 Starting Truth or Dare! 🎉\n")
    while True:
        player = random.choice(players)
        print(f"\n👉 It's {player}'s turn!")
        choice = input("Type 'truth', 'dare', or 'quit' to end: ").strip().lower()

        if choice == 'truth':
            print("🧠 Truth:", random.choice(truths))
        elif choice == 'dare':
            print("🎯 Dare:", random.choice(dares))
        elif choice == 'quit':
            print("Thanks for playing!")
            break
        else:
            print("Invalid input. Please type 'truth', 'dare', or 'quit'.")
        time.sleep(1.5)

#For AI connectivity
def ask_me(prompt):
    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",  # Or use any other Together-supported model
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Together SDK error: {e}"

# For music playing todo:add program to play selected music from downloads

def list_songs_in_downloads():
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    audio_extensions = ('.mp3', '.aac', '.ogg', '.m4a', '.wav')
    songs = [f for f in os.listdir(downloads_path) if f.endswith(audio_extensions)]
    return songs, downloads_path

def play_song(song_path):
    if sys.platform == 'win32':
         os.startfile(song_path)
    elif sys.platform == 'darwin':
        subprocess.call(['open', song_path])
    else:  #For Linux
        subprocess.call(["xdg-open", song_path])

def choose_and_play_song():
    songs, downloads_path = list_songs_in_downloads()
    if not songs:
        say("Sorry, I couldn't find any songs.")
        return

    say ("Please say the name of the song that you want to play.")
    query = takeCommand().lower()

#To find the fuzzy matching song
    close_matches = difflib.get_close_matches(query, songs, n=1, cutoff=0.7)

    if close_matches:
        selected_song = os.path.join(downloads_path, close_matches[0])
        say(f"Playing {close_matches[0]}")
        play_song(selected_song)
    else:
        say("I couldn't find a matching song. Here's your list of songs. please choose a number.")
        for idx, song in enumerate(songs):
            print(f"{idx+1}. {song}")
            say(f"{idx+1}. {song}")

    try:
        say("Please say the number of the song you want to play.")
        choice_text = takeCommand()
        if choice_text.isdigit():
            choice = int(choice_text)
            if 1 <= choice <= len(songs):
                selected_song = os.path.join(downloads_path, songs[choice - 1])
                play_song(selected_song)
            else:
                say("Invalid choice number.")
        else:
            say("that was not a valid number.")
    except Exception as e:
        say("something went wrong while playing the song.")
        print("error:", e)

#Initialisation of Xebec (core function) & shutting down
def run_Xebec():
    say("Hello, I am Xebec")
    say("I've been awakened")

    while True:
        query = takeCommand()
        if not query:
            continue

        query = query.lower()


        if any(cmd in query for cmd in ["stop", "quit", "exit", "shut down"]):
            say("Are you sure you want to shut down?")
            confirmation = takeCommand()

            if any(word in confirmation for word in ["yes", "sure", "okay", "do it"]):
                say("Shutting down...")
                return "stop"

            elif any(word in confirmation for word in ["no", "nope","cancel","wait"]):
                say("shutdown cancelled. I'm still here.")
                continue

        elif "play song" in query or "play music" in query:
            choose_and_play_song()

        elif "switch to" in query and "voice" in query:
            voice_name =query.replace("switch to", "").replace("voice", "").strip()
            if voice_name:
                set_voice_by_name(voice_name)
            else:
                say("please say the name.")

# For creation of word documents.
        elif "create document" in query or "write article" in query:
            say("What topic should i write about?")
            topic = takeCommand()
            if topic:
                create_word_doc_from_topic(topic)
            else:
                say("I didn't catch the topic. Please try again.")

# For Time
        elif "the time" in query:
            strfTime = datetime.datetime.now().strftime('%I:%M %p')
            say(f"The time is {strfTime}")

#For opening sites todo: add more sites
        elif "open" in query:
            sites = {
                "youtube": "https://www.youtube.com",
                "instagram": "https://www.instagram.com",
                "facebook": "https://www.facebook.com",
                "google": "https://www.google.com",
                "chat gpt": "https://www.chatgpt.com",
                "spotify": "https://www.spotify.com",
                "github": "https://www.github.com",
                "deepseek": "https://www.deepseek.com",
                "canva": "https://www.canva.com",
                "whatsapp": "https://www.whatsapp.com",
                "discord": "https://www.discord.com",
                
            }
            opened = False
            for site in sites:
                if f"open {site}" in query:
                    say(f"Opening {site}...")
                    webbrowser.open(sites[site])
                    opened = True
                    break
            if not opened:
                say("Sorry, I don't recognize that site , or it may not be in my data.")

#To Start & Triger Truth and dare
        elif "truth or dare" in query:
            say("Starting Truth or Dare game.")
            players = get_players()
            if players:
                play_game(players)
            else:
                say("No players entered. Exiting game.")

#For selection of games
        elif "play game" in query:
            say("Which game would you like to play? You can say Number Guessing.")
            game_choice = takeCommand()
            if "number" in game_choice or "guess" in game_choice:
                number_guessing_game()
            else:
                say("Sorry, I only know the number guessing game for now.")

        elif any(x in query for x in ["who is ", "has", "what is", "tell me about", "define", "ask me"]):
            answer = ask_me(query)
            print("ChatGpt:", answer)
            say(answer)

# Main loop to run Xebec
if __name__ == '__main__': #to ensure main loop doesn't auto-run on import
    while True:
        status = run_Xebec()
        if status in ["stop" , "quit", "exit", "shut down"]:
            say("Going offline...")
            break


