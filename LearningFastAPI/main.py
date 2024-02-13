import threading

from fastapi import FastAPI, BackgroundTasks, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from logic.FrameGenerator import FrameGenerator
# from geofence.FrameGenerator import FrameGenerator
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


@app.get("/video_feed")
async def video_feed(camera_id: int,conn_str:str,height:str,width:str):
    if camera_id not in frame_generators:
        # If FrameGenerator instance doesn't exist for this camera_id, create a new one
        # if camera_id==1:
        #     url_rtsp = f'rtsp://admin:Trace3@123@192.168.1.64:554'
        # else:
        #     url_rtsp = f'rtsp://admin:Trace3@123@192.168.1.65:554'

        frame_generators[camera_id] = FrameGenerator(camera_id=camera_id, url_rtsp=conn_str,height=height,width=width)

    frame_generator = frame_generators[camera_id]
    return StreamingResponse(frame_generator.generate_frames(), media_type="multipart/x-mixed-replace;boundary=frame")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=False)
