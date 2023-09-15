
import pygame.mixer
import threading

# Initialize the mixer module
pygame.mixer.init()

# Create a Sound object from your WAV file
sound_danger = pygame.mixer.Sound('logic/danger_alert.wav')

# Flag to control whether the sound alert is active
danger_sound_event = threading.Event()

# Function to play the danger sound
def play_danger_sound():
    print("Playing danger sound")
    while not danger_sound_event.is_set():
        sound_danger.play()

# Function to start the danger sound alert
def start_danger_alert():
    print("Starting danger alert")
    danger_sound_event.clear()
    play_danger_thread = threading.Thread(target=play_danger_sound)
    play_danger_thread.start()

# Function to stop the danger sound alert
def stop_danger_alert():
    print("Stopping danger alert")
    danger_sound_event.set()
    sound_danger.stop()