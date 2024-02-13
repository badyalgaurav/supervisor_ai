from fastapi import APIRouter
from geofence import mongo_op
from geofence.schemas.polygon_info_schemas import PolygonInfoSchemas

router = APIRouter(prefix="/mongo_op", tags=["mongo_op"])


@router.get("/get_polygon")
async def get_polygon(camera_no: int):
    res = mongo_op.get_polygon(camera_no=camera_no)
    return res


@router.post("/upsert_polygon")
async def upsert_polygon(model: PolygonInfoSchemas):
    camera_no = model.camera_no
    polygon_info = model.polygon_info
    res = mongo_op.upsert_polygon(camera_no=camera_no, polygon_info=polygon_info)
    return res
