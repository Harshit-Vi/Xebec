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


# text-to-speech engine
engine = pyttsx3.init()

# Initialize Together client (direct key or from environment)
together_api_key = "tgp_v1_RSVq1hWYbQbyGMussZ57xgLB5yZ_ArpuaHW-TnG36Hk"
client = Together(api_key=together_api_key)

# voice recognition , Interpretation & voice to text .
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

        filename = f"{topic.replace(' ', '_')}.docx"
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

#Initialisation of Xebec & shutting down
def run_Xebec():
    say("Hello, I am Xebec")
    say("I've been awakened")

    while True:
        query = takeCommand()

        if "stop" in query:
            say("Shutting down...")
            return "stop"

# For music playing todo:add program to play selected music from downloads
        elif "play music" in query:
            say("Playing your music now!")
            musicPath = r"C:\Users\Harshit Singh\Downloads\CHOOT VOL. 1 - Yo Yo Honey Singh Ft. Badshah (Official Music Video) - Mafia Mundeer.mp3"
            os.startfile(musicPath)

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

            }

            for site in sites:
                if f"open {site}" in query:
                    say(f"Opening {site}...")
                    webbrowser.open(sites[site])
                    break

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
while True:
    status = run_Xebec()
    if status == "stop":
        say("Going offline...")
        break

