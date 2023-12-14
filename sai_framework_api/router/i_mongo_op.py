from fastapi import APIRouter
from fastapi.responses import  FileResponse
from logic import mongo_op
import json
from logic.schemas.polygon_info_schemas import PolygonInfoSchemas

router = APIRouter(prefix="/mongo_op", tags=["mongo_op"])


@router.get("/get_polygon")
async def get_polygon():
    res = mongo_op.get_polygon()
    return res


@router.get("/get_alert_counts")
async def get_alert_counts():
    res = mongo_op.get_alert_counts()
    return res


@router.get("/get_alert_details")
async def get_alert_details(camera_id: int, start_date: str, end_date: str):
    res = mongo_op.get_alert_details(camera_id=camera_id, start_date=start_date, end_date=end_date)
    return res


@router.post("/upsert_polygon")
async def upsert_polygon(model: PolygonInfoSchemas):
    camera_no = model.camera_no
    polygon_info = json.loads(model.polygon_info)
    res = mongo_op.upsert_polygon(camera_no=camera_no, polygon_info=polygon_info,start_time=model.start_time,end_time=model.end_time)

    return res


@router.get("/video")
async def get_video(video_path):
    # Replace 'path_to_video.mp4' with the actual path to your video file.
    # video_path = "/var/www/camera_3_939715_video.mp4"
    return FileResponse(video_path, media_type="video/mp4")

@router.get("/get_time_data")
async def get_time_data():
    res = mongo_op.get_time_data()
    return res