from fastapi import APIRouter
from logic.business import b_alert

router = APIRouter(prefix="/alert", tags=["alert"])

alert_b = b_alert.Alert()


@router.get("/get_alert_counts")
async def get_alert_counts(user_id:str):
    res = alert_b.get_alert_counts(user_id=user_id)
    return res


@router.get("/get_alert_details")
async def get_alert_details(user_id:str, camera_id: int, start_date: str, end_date: str):
    res = alert_b.get_alert_details(user_id=user_id,camera_id=camera_id, start_date=start_date, end_date=end_date)
    return res
