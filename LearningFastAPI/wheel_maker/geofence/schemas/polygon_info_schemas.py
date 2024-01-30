from typing import Optional
from pydantic import BaseModel


class PolygonInfoSchemas(BaseModel):
    camera_no: Optional[int] = None
    polygon_info: Optional[str] = None

