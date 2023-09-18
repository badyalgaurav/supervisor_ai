# from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect
# import uvicorn
# from fastapi.middleware.cors import CORSMiddleware
# import cv2
# import asyncio
# from router.i_interface import router as api_router
# app = FastAPI()
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
#     allow_credentials=True
# )
# app.include_router(api_router)
# ##----------------------------------------------LIVE CAMERA------------------------
#
# from logic import human_detection
# from queue import Queue, Empty
# from threading import Thread
#
# # Replace with your Hikvision camera's IP address and RTSP port
# camera_ip = '192.168.1.64'
# rtsp_port = '554'
# username = 'admin'  # Replace with your camera's username
# password = 'Trace3@123'  # Replace with your camera's password
#
# # Hikvision camera URL with authentication
# camera_url = f'rtsp://{username}:{password}@{camera_ip}:{rtsp_port}/Streaming/Channels/1'
#
# # Video frame buffer queue
# frame_queue = Queue(maxsize=50)  # Adjust the buffer size as needed
# # Global counter for frame skipping
# global frame_counter
# frame_counter = 0  # Initialize frame_counter as a global variable
#
#
# # Function to read frames and put them into the buffer
# def read_frames():
#     cap = cv2.VideoCapture(camera_url, cv2.CAP_FFMPEG)
#     while True:
#         success, frame = cap.read()
#         if not success:
#             print("camera stopped sending the frames")
#             read_frames()
#             # break
#         frame_queue.put(frame)
#
#
# # Start the frame reading thread
# frame_thread = Thread(target=read_frames)
# frame_thread.daemon = True
# frame_thread.start()
#
#
# # Close the frame thread when the application stops
# @app.on_event("shutdown")
# def close_frame_thread():
#     frame_thread.join()
#
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
#
# #################workingfine###################
# # @app.websocket("/ws1/{camera_id}")
# # async def working_fine_without_object_detection_get_stream(websocket: WebSocket, camera_id: int):
# #     await websocket.accept()
# #     try:
# #         while True:
# #             try:
# #                 # Get a frame from the buffer (frame skipping)
# #                 frame = frame_queue.get(timeout=2)  # Adjust the timeout as needed
# #             except Empty:
# #                 continue
# #             ret, buffer = cv2.imencode('.jpg', frame)
# #             await websocket.send_bytes(buffer.tobytes())
# #             await asyncio.sleep(0.1)
# #     except WebSocketDisconnect:
# #         print("Client disconnected")
#
# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)



from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import cv2
import asyncio
from queue import Queue
from threading import Thread
from logic import human_detection

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Replace with your Hikvision camera's IP address and RTSP port
camera_ip = '192.168.1.64'
rtsp_port = '554'
username = 'admin'  # Replace with your camera's username
password = 'Trace3@123'  # Replace with your camera's password

# Hikvision camera URL with authentication
camera_url = f'rtsp://{username}:{password}@{camera_ip}:{rtsp_port}/Streaming/Channels/1'

# Video frame buffer queue
frame_queue = Queue(maxsize=50)  # Adjust the buffer size as needed

# Global frame skipping settings
frame_skip_interval = 3  # Skip every 3 frames
frame_counter = 0

# Function to read frames and put them into the buffer
def read_frames():
    cap = cv2.VideoCapture(camera_url, cv2.CAP_FFMPEG)
    while True:
        success, frame = cap.read()
        if not success:
            print("Camera stopped sending frames. Reconnecting...")
            cap.release()
            cap = cv2.VideoCapture(camera_url, cv2.CAP_FFMPEG)
            continue
        frame_queue.put(frame)

# Start the frame reading thread
frame_thread = Thread(target=read_frames)
frame_thread.daemon = True
frame_thread.start()

# Close the frame thread when the application stops
@app.on_event("shutdown")
def close_frame_thread():
    frame_thread.join()

# WebSocket endpoint for streaming with object detection
@app.websocket("/ws1/{camera_id}")
async def streaming_with_object_detection(websocket: WebSocket, camera_id: int):
    await websocket.accept()
    global frame_counter

    while True:
        try:
            # Get a frame from the buffer (frame skipping)
            frame = frame_queue.get(timeout=2)  # Adjust the timeout as needed
            frame_counter += 1
            if frame_counter % frame_skip_interval != 0:
                continue
            frame_counter = 0

            # Resize frame to a smaller resolution
            frame = cv2.resize(frame, (820, 460))  # Adjust the resolution as needed

            # Perform object detection on the frame using YOLO
            resized_frame = await asyncio.to_thread(human_detection.detect_yolo_person_in_polygon, frame)
        except asyncio.TimeoutError:
            print("Frame retrieval timeout.")
            continue
        except WebSocketDisconnect:
            print("Client disconnected.")
            break
        ret, buffer = cv2.imencode('.jpg', resized_frame)
        await websocket.send_bytes(buffer.tobytes())
        await asyncio.sleep(0.01)  # Adjust the sleep time as needed for desired frame rate

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
