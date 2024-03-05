# from imutils.video import VideoStream
from pymongo import MongoClient
import pandas as pd
# import numpy as np
from shapely.geometry import Polygon


def GetClientUpdateByComapnyCode():
    serverAddress = "127.0.0.1:27017"
    client = MongoClient(f"mongodb://{serverAddress}")
    return client


def get_all_polygon():
    client = GetClientUpdateByComapnyCode()
    db = client["supervisorAI"]
    coll = db["polygonInfo"]
    df = pd.DataFrame(coll.find({}, {"_id": 0}))
    # Loop over the rows using iterrows()
    response = {}

    for index, row in df.iterrows():
        polygon_list = []
        recPoly_dict = {}
        for polygon in row["polygonInfo"]:
            result = Polygon([(item['x'], item['y']) for item in polygon.get("polygon")])
            if polygon.get("label") == "recPoly":
                recPoly_dict = result
            else:
                polygon_list.append(result)
        response[row.get("camera_no")] = {"polygon_list": polygon_list, "recPoly_dict": recPoly_dict, "start_time": row.get("startTime"), "end_time": row.get("endTime")}

    print("successfully data loaded")
    return response


def insert_events_db(camera_id, video_path, start_time, end_time):
    client = GetClientUpdateByComapnyCode()
    db = client["supervisorAI"]
    coll = db["productionData"]
    coll.insert_one({"cameraId": camera_id, "videoPath": video_path, "startTime": start_time, "endTime": end_time, "fileSize": -1})
    return True
