from fastapi import APIRouter
from router import i_geofence
from router import i_alert

router = APIRouter()
router.include_router(i_geofence.router)
router.include_router(i_alert.router)
