from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import uvicorn
import asyncio
import imutils
from imutils.video import VideoStream
from logic import human_detection
from logic.mongo_op import get_all_polygon

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

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



# Configuration
# camera_ip = '192.168.1.64'
# rtsp_port = '554'
# username = 'admin'
# password = 'Trace3@123'
url_rtsp_1 = f'rtsp://admin:Trace3@123@192.168.1.64:554'

frame_counter = 0  # Initialize frame_counter as a global variable

vs = VideoStream(url_rtsp_1).start()
async def generate_frames(camera_id):
    global frame_counter

    # await asyncio.sleep(2)  # Allow time for the camera to initialize
    try:
        while True:
            frame = vs.read()
            frame = imutils.resize(frame, width=820,height=534)

            if frame is not None:
                frame_counter += 1
                poly_info = database_data.get(camera_id)
                poly_info = poly_info[:2]
                danger_zone_poly = 1 if len(poly_info) > 1 else 0
                if frame_counter % 7 == 0:
                    await asyncio.to_thread(human_detection.detect_yolo_person_in_polygon, camera_id, frame, poly_info, danger_zone_poly)
                    frame_counter = 0
                else:
                    await asyncio.to_thread(human_detection.from_box_person_in_polygon, camera_id, frame, poly_info, danger_zone_poly)
                _, buffer = cv2.imencode(".jpg", frame)
                frame_bytes = buffer.tobytes()
                await asyncio.sleep(0)
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    except:
        generate_frames(camera_id)

@app.get("/video_feed")
async def video_feed(camera_id:int):
    return StreamingResponse(generate_frames(camera_id), media_type="multipart/x-mixed-replace;boundary=frame")

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=False)
