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


url_rtsp_1 = f'rtsp://admin:Trace3@123@192.168.1.64:554'
url_rtsp_2 = f'rtsp://admin:Trace3@123@192.168.1.64:554'
url_rtsp_3 = f'rtsp://admin:Trace3@123@192.168.1.64:554'
url_rtsp_4 = f'rtsp://admin:Trace3@123@192.168.1.64:554'

# Create VideoStream instances for each camera
camera_streams = {
    1: VideoStream(url_rtsp_1).start(),
    2: VideoStream(url_rtsp_2).start(),
    3: VideoStream(url_rtsp_3).start(),
    4: VideoStream(url_rtsp_4).start(),
}

frame_counters = {1: 0, 2: 0, 3: 0, 4: 0}

# Create a dictionary to store thread termination flags
thread_termination_flags = {1: False, 2: False, 3: False, 4: False}



async def generate_frames(camera_id):
    try:
        while not thread_termination_flags[camera_id]:
            frame = camera_streams[camera_id].read()
            frame = imutils.resize(frame, width=820, height=534)

            if frame is not None:
                frame_counters[camera_id] += 1
                poly_info = database_data.get(camera_id)
                poly_info = poly_info[:2]
                danger_zone_poly = 1 if len(poly_info) > 1 else 0
                if frame_counters[camera_id] % 7 == 0:
                    await asyncio.to_thread(human_detection.detect_yolo_person_in_polygon, camera_id, frame, poly_info, danger_zone_poly)
                    frame_counters[camera_id] = 0
                else:
                    await asyncio.to_thread(human_detection.from_box_person_in_polygon, camera_id, frame, poly_info, danger_zone_poly)
                _, buffer = cv2.imencode(".jpg", frame)
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    except:
        pass  # Handle exceptions as needed

def stop_stream(camera_id):
    camera_streams[camera_id].stop()

@app.on_event("shutdown")
def stop_streams():
    # Release all camera streams on server shutdown
    for camera_id in camera_streams:
        thread_termination_flags[camera_id] = True
        stop_stream(camera_id)

@app.get("/video_feed")
async def video_feed(camera_id: int):
    if camera_id in camera_streams:
        thread_termination_flags[camera_id] = False  # Reset the termination flag
        return StreamingResponse(generate_frames(camera_id), media_type="multipart/x-mixed-replace;boundary=frame")
    else:
        return "Camera not found"

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=False)
