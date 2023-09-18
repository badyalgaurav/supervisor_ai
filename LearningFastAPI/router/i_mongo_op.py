from fastapi import APIRouter
from logic import mongo_op

router = APIRouter(prefix="/mongo_op", tags=["mongo_op"])


@router.get("/get_polygon")
async def get_polygon(camera_no: int):
    res = mongo_op.get_polygon(camera_no=camera_no)
    return res


@router.get("/upsert_polygon")
async def upsert_polygon(polygon_info: str, camera_no: int):
    res = mongo_op.upsert_polygon(camera_no=camera_no, polygon_info=polygon_info)
    return res
