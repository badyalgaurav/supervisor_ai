import asyncio

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import cv2
from starlette.background import BackgroundTasks

from logic.FrameGenerator import FrameGenerator
from logic.schemas.init_inp_schemas import InitInpSchemas

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


@app.post("/init_api")
async def init_api(model: InitInpSchemas, background_tasks: BackgroundTasks):
    background_tasks.add_task(video_feed_bg, model.user_id, model.camera_id, model.conn_str, model.height, model.width, model.ai_per_second)
    return "success"


async def video_feed_bg(user_id: str, camera_id: int, conn_str: str, height: str, width: str, ai_per_second: int):
    if camera_id not in frame_generators:
        frame_generators[camera_id] = FrameGenerator(user_id=user_id, camera_id=camera_id, url_rtsp=conn_str, height=height, width=width, ai_per_second=ai_per_second)
    frame_generator = frame_generators[camera_id]
    await frame_generator.generate_frames_bg()


@app.get("/video_feed")
async def video_feed(user_id: str, camera_id: int, conn_str: str, height: str, width: str, ai_per_second: int, background_tasks: BackgroundTasks):
    async def generate():
        try:
            while True:
                frame = frame_generators[camera_id].display_frame
                if frame is not None:
                    _, buffer = cv2.imencode(".jpg", frame)
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n' b'Content-Type: image/jpg\r\n\r\n' + frame_bytes + b'\r\n')
                await asyncio.sleep(1)  # Adjust sleep time as needed
        except Exception as e:
            print(f"ERROR: {e}")
            raise Exception("An error occurred while generating frames")

    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace;boundary=frame")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=15002)
