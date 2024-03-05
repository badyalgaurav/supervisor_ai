from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import cv2
import asyncio

from logic.mongo_op import get_all_polygon

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)
##----------------------------------------------LIVE CAMERA------------------------

from logic import human_detection
from queue import Queue, Empty
from threading import Thread

# Replace with your Hikvision camera's IP address and RTSP port
camera_ip = '192.168.1.64'
rtsp_port = '554'
username = 'admin'  # Replace with your camera's username
password = 'Trace3@123'  # Replace with your camera's password

# Hikvision camera URL with authentication
camera_url = f'rtsp://{username}:{password}@{camera_ip}:{rtsp_port}/Streaming/Channels/1'

# Video frame buffer queue
frame_queue = Queue(maxsize=1)  # Adjust the buffer size as needed
# Global counter for frame skipping
global frame_counter
frame_counter = 0  # Initialize frame_counter as a global variable


# Function to read frames and put them into the buffer
def read_frames():
    cap = cv2.VideoCapture(camera_url, cv2.CAP_FFMPEG)
    while True:
        success, frame = cap.read()
        if not success:
            print("Camera stopped sending frames")
            # You can choose to exit the loop or take other appropriate action
            break
        # Clear the queue before putting the latest frame to ensure only the latest frame is in the queue
        while not frame_queue.empty():
            try:
                frame_queue.get_nowait()
            except Empty:
                continue
        frame_queue.put(frame)


# Start the frame reading thread
frame_thread = Thread(target=read_frames)
frame_thread.daemon = True
frame_thread.start()

# Define a global variable to store the data
database_data = None


async def fetch_data_periodically():
    while True:
        # Retrieve data from the database
        new_data = get_all_polygon()  # Replace with your actual query
        # Update the global data with the new data
        global database_data
        database_data = new_data
        # Sleep for 5 minutes before checking again
        await asyncio.sleep(300)  # 300 seconds = 5 minutes


@app.on_event("startup")
async def startup_event():
    # Start the background task to fetch data periodically
    asyncio.create_task(fetch_data_periodically())


# Close the frame thread when the application stops
@app.on_event("shutdown")
async def close_frame_thread():
    frame_thread.join()


@app.websocket("/ws1/{camera_id}")
async def working_fine_with_object_detection_get_stream(websocket: WebSocket, camera_id: int):
    global database_data  # Access the global data
    await websocket.accept()
    global frame_counter
    try:
        while True:
            try:
                poly_info = database_data.get(camera_id)
                poly_info = poly_info[:2]
                danger_zone_poly= 1 if len(poly_info) > 1 else 0
                # Get a frame from the buffer (frame skipping)
                frame = frame_queue.get(timeout=1, block=True)  # Adjust the timeout as needed
                frame_counter += 1
                if frame_counter % 3 != 0:
                    continue
                frame_counter = 0
                # Resize frame to a smaller resolution
                frame = cv2.resize(frame, (820, 534))  # Adjust the resolution as needed

                resized_frame = await asyncio.to_thread(human_detection.detect_yolo_person_in_polygon, camera_id,frame,poly_info,danger_zone_poly)
            except Empty:
                continue
            ret, buffer = cv2.imencode('.jpg', frame)
            await websocket.send_bytes(buffer.tobytes())
            # await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)
