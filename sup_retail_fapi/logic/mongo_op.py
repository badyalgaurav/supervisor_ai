# from imutils.video import VideoStream
# from pymongo import MongoClient
import threading
import time

import pandas as pd
# import numpy as np
from shapely.geometry import Polygon
import requests

from logic.communicator.email_sender import send_video_email

SUP_API_URL = "http://interx.ai/api_sup"


def get_all_polygon(user_id: str):
    res = {}
    try:
        url = f"{SUP_API_URL}/geofence/get_all_polygon"
        data = {"user_id": user_id}
        response = requests.get(url, data)
        if response.status_code == 200:
            result = response.json()
            df = pd.DataFrame(result)
            for index, row in df.iterrows():
                polygon_list = []
                rec_poly_dict = {}
                for polygon in row["polygonInfo"]:
                    result = Polygon([(item['x'], item['y']) for item in polygon.get("polygon")])
                    if polygon.get("label") == "recPoly":
                        rec_poly_dict = result
                    else:
                        polygon_list.append(result)
                res[row.get("camera_no")] = {"polygon_list": polygon_list, "recPoly_dict": rec_poly_dict, "start_time": row.get("startTime"), "end_time": row.get("endTime")}
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
            print("Error message:", response.text)
    except Exception as e:
        print(f"ERROR: ${e}")
    return res


def insert_events_db(user_id: str, camera_id: int, video_path: str, start_time: str, end_time: str):
    url = f"{SUP_API_URL}/geofence/insert_events_db"
    data = {"user_id": user_id, "camera_id": int(camera_id), "video_path": video_path, "start_time": str(start_time), "end_time": str(end_time)}

    response = requests.get(url, data)
    if response.status_code == 200:

        result = response.json()
        email_thread = threading.Thread(target=send_email, args=(user_id, video_path))
        email_thread.start()
        print("API Response:", result)
    else:
        print(f"Failed to send data. Status code: {response.status_code}")
        print("Error message:", response.text)
    return True


def send_email(user_id: str, video_path: str):
    try:
        # Create a new thread to send the email
        user_info = get_user_info_by_id(user_id)
        # sender_email_list=[]
        # sender_email_list.append(user_info.get("cEmail"))
        sender_email_list=user_info.get("notificationEmails")
        sender_email_list.append("badyalgaurav0@gmail.com")
        sender_email_list.append("sahilloria34@gmail.com")
        # time.sleep(5)
        send_video_email(sender_email_list, video_path)
    except Exception as e:
        print(f"ERROR: {e}")


def get_user_info_by_id(user_id: str):
    url = f"{SUP_API_URL}/gemmiz/get_user_info_by_id"
    data = {"user_id": user_id}

    response = requests.get(url, data)
    if response.status_code == 200:
        result = response.json()
        print("API Response:", result)
    else:
        print(f"Failed to send data. Status code: {response.status_code}")
        print("Error message:", response.text)
    return result
