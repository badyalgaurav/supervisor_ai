import asyncio

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import cv2
from starlette.background import BackgroundTasks

from logic.FrameGenerator import FrameGenerator

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# Dictionary to store FrameGenerator instances based on camera_id
frame_generators = {}
recent_frames = {}


@app.get("/video")
async def get_video(video_path):
    return FileResponse(video_path, media_type="video/mp4")


@app.get("/init_api")
async def init_api(user_id: str, camera_id: int, conn_str: str, height: str, width: str, ai_per_second: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(video_feed_bg, user_id, camera_id, conn_str, height, width, ai_per_second)
    return "success"


async def video_feed_bg(user_id: str, camera_id: int, conn_str: str, height: str, width: str, ai_per_second: int):
    if camera_id not in frame_generators:
        frame_generators[camera_id] = FrameGenerator(user_id=user_id, camera_id=camera_id, url_rtsp=conn_str, height=height, width=width, ai_per_second=ai_per_second)
    frame_generator = frame_generators[camera_id]
    await frame_generator.generate_frames_bg()


@app.get("/video_feed")
async def video_feed(user_id: str, camera_id: int, conn_str: str, height: str, width: str, ai_per_second: int, background_tasks: BackgroundTasks):
    async def generate():
        while True:
            try:
                frame = frame_generators[camera_id].display_frame
            except KeyError as e:
                init_api(user_id, camera_id, conn_str, height, width, ai_per_second)
            except Exception as e:
                print("Error occurred during initialization:", e)

            if frame is not None:
                _, buffer = cv2.imencode(".jpg", frame)
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpg\r\n\r\n' + frame_bytes + b'\r\n')
            await asyncio.sleep(0.001)  # Adjust sleep time as needed

    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace;boundary=frame")


# @app.get("/video_feed")
# async def video_feed(user_id: str, camera_id: int, conn_str: str, height: str, width: str, ai_per_second: int, background_tasks: BackgroundTasks):
#     if camera_id not in frame_generators:
#         frame_generators[camera_id] = FrameGenerator(user_id=user_id, camera_id=camera_id, url_rtsp=conn_str, height=height, width=width, ai_per_second=ai_per_second)
#     frame_generator = frame_generators[camera_id]
#     return StreamingResponse(frame_generator.generate_frames(), media_type="multipart/x-mixed-replace;boundary=frame")

if __name__ == '__main__':    uvicorn.run(app, host="0.0.0.0", port=8000)
