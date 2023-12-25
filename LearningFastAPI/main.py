from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import uvicorn
import asyncio
import imutils
from imutils.video import VideoStream
# from logic import human_detection
# from fastapi import BackgroundTasks

from logic.human_detection_class import CameraProcessor
from logic.mongo_op import get_all_polygon, get_camera_settings
import time

# import signal
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


# camera_streams=None

async def fetch_data_periodically():
    while True:
        # Retrieve data from the database
        new_data = get_all_polygon()  # Replace with your actual query
        # Update the global data with the new data
        global database_data
        database_data = new_data
        # Sleep for 5 minutes before checking again
        await asyncio.sleep(120)  # 300 seconds = 5 minutes


@app.on_event("startup")
async def startup_event():
    # signal.signal(signal.SIGINT, stop_stream)
    # Start the background task to fetch data periodically

    asyncio.create_task(fetch_data_periodically())
    # global camera_streams
    # camera_streams = get_camera_settings()


#
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


# FOR CLASS SOLUTION
async def generate_frames(camera_id, background_tasks: BackgroundTasks):
    camera_processor = CameraProcessor(camera_id)
    # camera_processor.start_video_writer()
    try:
        while not thread_termination_flags[camera_id]:
            frame = camera_streams[camera_id].read()

            if frame is not None:
                frame = imutils.resize(frame, width=812, height=534)
                frame_counters[camera_id] += 1
                poly_info = database_data.get(camera_id).get("polygon_list")
                rec_poly_info = database_data.get(camera_id).get("recPoly_dict")

                if frame_counters[camera_id] % 10 == 0:
                    await asyncio.to_thread(camera_processor.detect_person_in_polygon, frame, poly_info, rec_poly_info)
                    frame_counters[camera_id] = 0
                else:
                    await asyncio.to_thread(camera_processor.from_box_person_in_polygon, frame, poly_info, rec_poly_info)

                # Yield frame for streaming response
                _, buffer = cv2.imencode(".jpg", frame)
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                camera_processor.write_frame_to_disk_async(frame)


    except Exception as e:
        print(f"Exception: {e}")
        pass
    finally:
        # Asynchronously release the video writer
        await asyncio.to_thread(camera_processor.release_video_writer)


@app.get("/video_feed")
async def video_feed(camera_id: int, background_tasks: BackgroundTasks):
    if camera_id in camera_streams:
        # thread_termination_flags[camera_id] = False  # Reset the termination flag
        return StreamingResponse(generate_frames(camera_id, background_tasks), media_type="multipart/x-mixed-replace;boundary=frame")
    else:
        return "Camera not found"


# def stop_stream(*args):
# for camera_id in camera_streams:
#     thread_termination_flags[camera_id] = True
#     # stop_stream(camera_id)
#     camera_streams[camera_id].stop()
#     print(f"stopped camera process {camera_id}")

def stop_stream(camera_id):
    camera_streams[camera_id].stop()
    print(f"stopped camera process {camera_id}")


def start_stream(camera_id):
    camera_streams[camera_id].start()


@app.on_event("shutdown")
def shutdown_event():
    # Release all camera streams on server shutdown
    for camera_id in camera_streams:
        thread_termination_flags[camera_id] = True
        stop_stream(camera_id)
    print("successfully data terminated")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=False)
