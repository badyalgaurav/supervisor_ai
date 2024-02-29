from fastapi import APIRouter
from router import i_geofence
from router import i_alert
from router import i_gemmiz

router = APIRouter()
router.include_router(i_geofence.router)
router.include_router(i_alert.router)
router.include_router(i_gemmiz.router)
