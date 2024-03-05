# from imutils.video import VideoStream
from pymongo import MongoClient
import pandas as pd
# import numpy as np
from shapely.geometry import Polygon
import requests

SUP_API_URL = "http://interx.ai/api_sup"


def GetClientUpdateByComapnyCode():
    serverAddress = "127.0.0.1:27017"
    client = MongoClient(f"mongodb://{serverAddress}")
    return client


def get_all_polygon(user_id: str):
    # client = GetClientUpdateByComapnyCode()
    # db = client["supervisorAI"]
    # coll = db["polygonInfo"]
    # df = pd.DataFrame(coll.find({}, {"_id": 0}))
    # # Loop over the rows using iterrows()
    # response = {}
    #
    # for index, row in df.iterrows():
    #     polygon_list = []
    #     recPoly_dict = {}
    #     for polygon in row["polygonInfo"]:
    #         result = Polygon([(item['x'], item['y']) for item in polygon.get("polygon")])
    #         if polygon.get("label") == "recPoly":
    #             recPoly_dict = result
    #         else:
    #             polygon_list.append(result)
    #     response[row.get("camera_no")] = {"polygon_list": polygon_list, "recPoly_dict": recPoly_dict, "start_time": row.get("startTime"), "end_time": row.get("endTime")}
    #
    # print("successfully data loaded")
    url = f"{SUP_API_URL}/geofence/get_all_polygon"
    data = {"user_id": user_id}

    response = requests.get(url, data)
    res = {}
    if response.status_code == 200:
        # Successful request, parse the response
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

        print("API Response:", result)
    else:
        print(f"Failed to send data. Status code: {response.status_code}")
        print("Error message:", response.text)

    return res


def insert_events_db(user_id: str, camera_id: int, video_path: str, start_time: str, end_time: str):
    # client = GetClientUpdateByComapnyCode()
    # db = client["supervisorAI"]
    # coll = db["productionData"]
    # coll.insert_one({"cameraId": camera_id, "videoPath": video_path, "startTime": start_time, "endTime": end_time, "fileSize": -1})

    url = f"{SUP_API_URL}/geofence/insert_events_db"
    data = {"user_id": user_id, "camera_id": int(camera_id), "video_path": video_path, "start_time": str(start_time), "end_time": str(end_time)}

    response = requests.get(url, data)
    if response.status_code == 200:
        result = response.json()
        print("API Response:", result)
    else:
        print(f"Failed to send data. Status code: {response.status_code}")
        print("Error message:", response.text)
    return True
