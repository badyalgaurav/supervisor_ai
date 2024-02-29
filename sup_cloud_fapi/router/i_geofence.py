import datetime

from fastapi import APIRouter
import json
from logic.business import b_geofence
from logic.schemas.polygon_info_schemas import PolygonInfoSchemas

router = APIRouter(prefix="/geofence", tags=["geofence"])

geofence_b = b_geofence.Geofence()


@router.get("/get_polygon")
async def get_polygon():
    res = geofence_b.get_polygon()
    return res


@router.post("/upsert_polygon")
async def upsert_polygon(model: PolygonInfoSchemas):
    camera_no = model.camera_no
    polygon_info = json.loads(model.polygon_info)
    res = geofence_b.upsert_polygon(camera_no=camera_no, polygon_info=polygon_info, start_time=model.start_time, end_time=model.end_time)
    return res


@router.get("/get_time_data")
async def get_time_data():
    print(datetime.datetime.now().second)
    res = geofence_b.get_time_data()
    print(datetime.datetime.now().second)

    return res
