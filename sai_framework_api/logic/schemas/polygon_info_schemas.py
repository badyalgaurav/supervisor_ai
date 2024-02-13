from typing import Optional
from pydantic import BaseModel


class PolygonInfoSchemas(BaseModel):
    camera_no: Optional[int] = None
    polygon_info: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None


class CameraInfo(BaseModel):
    cName: Optional[str] = None
    cEmail: Optional[str] = None
    cAddress: Optional[str] = None
    cPassword: Optional[str] = None

    eName: Optional[str] = None
    eEmail: Optional[str] = None
    eAddress: Optional[str] = None

    cameraInfo: Optional[str] = None
