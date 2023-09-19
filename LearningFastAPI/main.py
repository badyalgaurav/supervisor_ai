from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import cv2
import asyncio
from router.i_interface import router as api_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)
app.include_router(api_router)
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
            print("camera stopped sending the frames")
            read_frames()
            # break
        frame_queue.put(frame)


# Start the frame reading thread
frame_thread = Thread(target=read_frames)
frame_thread.daemon = True
frame_thread.start()


# Close the frame thread when the application stops
@app.on_event("shutdown")
def close_frame_thread():
    frame_thread.join()

# @app.websocket("/ws1/{camera_id}")
# async def working_fine_with_object_detection_get_stream(websocket: WebSocket, camera_id: int):
#     await websocket.accept()
#     global frame_counter
#     try:
#         while True:
#             try:
#                 # Get a frame from the buffer (frame skipping)
#                 frame = frame_queue.get(timeout=2)  # Adjust the timeout as needed
#                 frame_counter += 1
#                 if frame_counter % 3 != 0:
#                     continue
#                 frame_counter = 0
#                 # Resize frame to a smaller resolution
#                 frame = cv2.resize(frame, (820, 460))  # Adjust the resolution as needed
#
#                 resized_frame = await asyncio.to_thread(human_detection.detect_yolo_person_in_polygon, frame)
#             except Empty:
#                 continue
#             ret, buffer = cv2.imencode('.jpg', frame)
#             await websocket.send_bytes(buffer.tobytes())
#             await asyncio.sleep(0.1)
#     except WebSocketDisconnect:
#         print("Client disconnected")




@app.websocket("/ws/{camera_id}")
async def get_stream(websocket: WebSocket, camera_id: int):
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    await websocket.accept()

    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                # Set the desired dimensions for the image
                new_width = 812
                new_height = 458
                resized_frame = cv2.resize(frame, (new_width, new_height))

                # Add a circle to the frame
                # circle_center = (320, 240)  # Center of the circle (x, y)
                # radius = 50  # Radius of the circle
                # circle_color = (0, 255, 0)  # Circle color in BGR format (green)
                # circle_thickness = 3  # Thickness of the circle's outline
                # cv2.circle(resized_frame, circle_center, radius, circle_color, circle_thickness)

                # resized_frame=human_detection.detect_yolo_person_only(img=resized_frame)
                # resized_frame=human_detection.detect_yolo_person_in_boundary(img=resized_frame,boundary_x1=12,boundary_y1=12,boundary_x2=408,boundary_y2=421)
                resized_frame = human_detection.detect_yolo_person_in_polygon(img=resized_frame)

                ret, buffer = cv2.imencode('.jpg', resized_frame)

                await websocket.send_bytes(buffer.tobytes())
                await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        print("Client disconnected")
    finally:
        camera.release()
#################workingfine###################
# @app.websocket("/ws1/{camera_id}")
# async def working_fine_without_object_detection_get_stream(websocket: WebSocket, camera_id: int):
#     await websocket.accept()
#     try:
#         while True:
#             try:
#                 # Get a frame from the buffer (frame skipping)
#                 frame = frame_queue.get(timeout=2)  # Adjust the timeout as needed
#             except Empty:
#                 continue
#             ret, buffer = cv2.imencode('.jpg', frame)
#             await websocket.send_bytes(buffer.tobytes())
#             await asyncio.sleep(0.1)
#     except WebSocketDisconnect:
#         print("Client disconnected")

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)





