import pygame

# Initialize the mixer
pygame.mixer.init()

# Load and play the audio file
pygame.mixer.music.load(r"")  # Replace with your actual filename
pygame.mixer.music.play()

# Wait until the sound has finished playing
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

