from typing import Optional
from pydantic import BaseModel


class InitInpSchemas(BaseModel):
    camera_id: Optional[int] = None
    polygon_info: Optional[str] = None
    user_id: Optional[str] = None
    conn_str: Optional[str] = None
    height: Optional[str] = None
    width: Optional[str] = None
    ai_per_second: Optional[int] = None

