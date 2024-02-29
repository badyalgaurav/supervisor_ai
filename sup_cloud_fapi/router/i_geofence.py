import datetime

from fastapi import APIRouter
import json
from logic.business import b_geofence
from logic.schemas.polygon_info_schemas import PolygonInfoSchemas

router = APIRouter(prefix="/geofence", tags=["geofence"])

geofence_b = b_geofence.Geofence()


@router.get("/get_polygon")
async def get_polygon(user_id: str):
    res = geofence_b.get_polygon(user_id=user_id)
    return res


@router.post("/upsert_polygon")
async def upsert_polygon(model: PolygonInfoSchemas):
    camera_no = model.camera_no
    polygon_info = json.loads(model.polygon_info)
    res = geofence_b.upsert_polygon(camera_no=camera_no, polygon_info=polygon_info, start_time=model.start_time, end_time=model.end_time, user_id=model.user_id)
    return res


@router.get("/get_all_polygon")
async def get_all_polygon(user_id: str):
    res = geofence_b.get_all_polygon(user_id=user_id)
    return res


@router.get("/get_time_data")
async def get_time_data(user_id: str):
    res = geofence_b.get_time_data(user_id=user_id)
    return res

@router.get("/insert_events_db")
async def insert_events_db(camera_id, video_path, start_time, end_time):
    res = geofence_b.insert_events_db(user_id=user_id,camera_id=camera_id,video_path= video_path, start_time=start_time, end_time=end_time)
    return res
