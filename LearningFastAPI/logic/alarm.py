import pygame.mixer
import threading

# Initialize the mixer module
pygame.mixer.init()

# Create Sound objects for different sound files
sound_files = {
    1: pygame.mixer.Sound('logic/danger_alert.wav'),
    2: pygame.mixer.Sound('logic/cam2.mp3'),
    3: pygame.mixer.Sound('logic/danger_alert.wav'),
    4: pygame.mixer.Sound('logic/danger_alert.wav')
}

# Create a dictionary to keep track of playing threads and events for each camera
camera_threads = {}
camera_events = {}

# Initialize the camera_events dictionary with threading.Event() objects
for camera_id in range(1, 5):
    camera_events[camera_id] = threading.Event()


# Function to play the sound for a specific camera
def play_camera_sound(camera_id):
    # print(f"Playing sound for camera {camera_id}")
    while not camera_events[camera_id].is_set():
        sound_files[camera_id].play()


# Function to start the sound alert for a specific camera
def start_camera_alert(camera_id):
    # print(f"Starting sound alert for camera {camera_id}")
    camera_events[camera_id].clear()
    camera_threads[camera_id] = threading.Thread(target=play_camera_sound, args=(camera_id,))
    camera_threads[camera_id].start()


# Function to stop the sound alert for a specific camera
def stop_camera_alert(camera_id):
    # print(f"Stopping sound alert for camera {camera_id}")
    camera_events[camera_id].set()
    sound_files[camera_id].stop()
