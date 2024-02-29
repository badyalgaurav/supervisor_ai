from pydantic import BaseModel
from typing import Optional


class CameraInfo(BaseModel):
    cName: Optional[str] = None
    cEmail: Optional[str] = None
    cAddress: Optional[str] = None
    cPassword: Optional[str] = None

    eName: Optional[str] = None
    eEmail: Optional[str] = None
    eAddress: Optional[str] = None

    cameraInfo: Optional[str] = None
