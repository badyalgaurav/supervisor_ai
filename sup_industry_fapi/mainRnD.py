from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import cv2
import time

from onvif import ONVIFCamera

from logic.gpt_model import chat_response, train_custom_model, res_from_custom_model, another_test_full_train_n_test, eleuther_ai_gpt_model_back
import io
import asyncio
from fastapi.responses import StreamingResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


@app.get("/")
async def root(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/chart_gpt")
async def chart_gpt(query: str):
    response = chat_response(query=query)
    return {"message": response}


@app.get("/train_gpt")
async def train_gpt():
    response = train_custom_model()
    return {"message": response}


@app.get("/res_cust_model")
async def res_cust_model(query):
    response = res_from_custom_model(query)
    return {"message": response}


@app.get("/another_test_full_train_n_test_api")
async def another_test_full_train_n_test_api(query):
    response = another_test_full_train_n_test(query)
    return {"message": response}


@app.get("/eleuther_ai_gpt_model")
async def eleuther_ai_gpt_model(query):
    response = eleuther_ai_gpt_model_back(query)
    return {"message": response}


@app.get("/eleuther_ai_gpt_model")
async def eleuther_ai_gpt_model(query):
    response = eleuther_ai_gpt_model_back(query)
    return {"message": response}


##----------------------------------------------LIVE CAMERA------------------------
# def generate_frames():
#     cap = cv2.VideoCapture(0)  # Use the camera index
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
#
#         # Add a delay to control the streaming speed
#         time.sleep(0.1)
#
#     cap.release()
#
# @app.get('/video_feed')
# def video_feed():
#     return Response(generate_frames(), media_type='multipart/x-mixed-replace; boundary=frame')


# camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#
#
# def generate():
#     # grab global references to the output frame and lock variables
#
#
#             while True:
#                 ret, frame = camera.read()
#                 if not ret:
#                     break
#                 # encode the frame in JPEG format
#                 (flag, encodedImage) = cv2.imencode(".jpg", frame)
#                 # ensure the frame was successfully encoded
#                 if not flag:
#                     continue
#                 # yield the output frame in the byte format
#                 yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
#                        bytearray(encodedImage) + b'\r\n')
#                 time.sleep(0.1)
#
# @app.get("/video_feed")
# def video_feed():
#     # return the response generated along with the specific media
#     # type (mime type)
#     # return StreamingResponse(generate())
#     return StreamingResponse(generate(), media_type="multipart/x-mixed-replace;boundary=frame")

from logic import human_detection


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
frame_queue = Queue(maxsize=50)  # Adjust the buffer size as needed
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
# async def get_stream_testing_object(websocket: WebSocket, camera_id: int):
#     await websocket.accept()
#     global frame_counter  # Access the global frame_counter
#     while True:
#         try:
#             # Get a frame from the buffer (frame skipping)
#             frame = frame_queue.get(timeout=1)  # Adjust the timeout as needed
#             # Increment frame counter
#             frame_counter += 1
#             # Skip every 10th frame for object detection
#             if frame_counter % 2 != 0:
#                 continue
#             # Reset frame counter after 10 frames
#             frame_counter = 0
#             # Assuming you have a function like detect_yolo_person_in_polygon
#             resized_frame = await asyncio.to_thread(human_detection.detect_yolo_person_in_polygon, frame)
#             ret, buffer = cv2.imencode('.jpg', frame)
#             await websocket.send_bytes(buffer.tobytes())
#             await asyncio.sleep(0.5)
#         except Empty:
#             continue
@app.websocket("/ws1/{camera_id}")
async def working_fine_without_object_detection_get_stream(websocket: WebSocket, camera_id: int):
    await websocket.accept()
    global frame_counter
    try:
        while True:
            try:
                # Get a frame from the buffer (frame skipping)
                frame = frame_queue.get(timeout=2)  # Adjust the timeout as needed
                frame_counter += 1
                if frame_counter % 3 != 0:
                    continue
                frame_counter = 0
                # Resize frame to a smaller resolution
                frame = cv2.resize(frame, (640, 360))  # Adjust the resolution as needed

                resized_frame = await asyncio.to_thread(human_detection.detect_yolo_person_in_polygon, frame)
            except Empty:
                continue
            ret, buffer = cv2.imencode('.jpg', frame)
            await websocket.send_bytes(buffer.tobytes())
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        print("Client disconnected")

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
