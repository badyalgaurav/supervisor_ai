from fastapi import APIRouter
from logic.business import b_gemmiz
from logic.schemas.camera_schemas import CameraInfo

router = APIRouter(prefix="/gemmiz", tags=["gemmiz"])

gemmiz_b = b_gemmiz.Gemmiz()


@router.post("/setup_registration")
async def setup_registration(data: CameraInfo):
    gemmiz_b.setup_registration(data)
    return {"message": "Form submitted successfully"}


@router.get("/get_camera_credentials")
async def get_camera_credentials(email: str, password: str):
    res = gemmiz_b.get_camera_credentials(email, password)
    return res
