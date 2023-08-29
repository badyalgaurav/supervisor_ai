from fastapi import FastAPI, Request,Response,WebSocket,WebSocketDisconnect
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import cv2
import time
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
                resized_frame=human_detection.detect_yolo_person_only(img=resized_frame)

                ret, buffer = cv2.imencode('.jpg', resized_frame)


                await websocket.send_bytes(buffer.tobytes())
                await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        print("Client disconnected")
    finally:
        camera.release()

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)

