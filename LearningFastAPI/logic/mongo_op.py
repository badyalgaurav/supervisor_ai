from imutils.video import VideoStream
from pymongo import MongoClient
import pandas as pd
import numpy as np
from shapely.geometry import Polygon


def GetClientUpdateByComapnyCode():
    serverAddress = "127.0.0.1:27017"
    client = MongoClient(f"mongodb://{serverAddress}")
    return client


def upsert_polygon(polygon_info: str, camera_no: int):
    client = GetClientUpdateByComapnyCode()
    db = client["supervisorAI"]
    coll = db["polygonInfo"]
    coll.update_one({"camera_no": camera_no}, {"$set": {"polygonInfo": polygon_info, "camera_no": camera_no}}, upsert=True)
    return True


def get_polygon(camera_no: int):
    res = {"data": None, "message": "MSG_100"}
    client = GetClientUpdateByComapnyCode()
    db = client["supervisorAI"]
    coll = db["polygonInfo"]
    res["data"] = coll.find_one({"camera_no": camera_no}, {"_id": 0})
    return res


# def get_camera_settings():
#     res = {"data": None, "message": "MSG_100"}
#     client = GetClientUpdateByComapnyCode()
#     db = client["supervisorAI"]
#     coll = db["cameraSettings"]
#     df = pd.DataFrame(coll.find({"isActive": True}, {"_id": 0}))
#     response = {}
#     for index, row in df.iterrows():
#         url = f'rtsp://{row.get("userName")}:{row.get("password")}@${row.get("address")}'
#         response[index + 1] = VideoStream(url).start()
#     return response


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
            # result = [(item['x'], item['y']) for item in polygon.get("polygon")]
            # result = np.array(result, dtype=np.int32)
            # result = result.reshape((-1, 1, 2))
            result = Polygon([(item['x'], item['y']) for item in polygon.get("polygon")])
            if polygon.get("label") == "recPoly":
                recPoly_dict = result
            else:
                polygon_list.append(result)
        response[row.get("camera_no")] = {"polygon_list": polygon_list, "recPoly_dict": recPoly_dict}

    print("successfully data loaded")
    return response


# def get_all_polygon():
#     client = GetClientUpdateByComapnyCode()
#     db = client["supervisorAI"]
#     coll = db["polygonInfo"]
#     df = pd.DataFrame(coll.find({}, {"_id": 0}))
#     # Loop over the rows using iterrows()
#     response = {}
#
#     for index, row in df.iterrows():
#         polygon_list = []
#         recPoly_dict = {}
#         for polygon in row["polygonInfo"]:
#             result = [(item['x'], item['y']) for item in polygon.get("polygon")]
#             result = np.array(result, dtype=np.int32)
#             result = result.reshape((-1, 1, 2))
#             if polygon.get("label") == "recPoly":
#                 recPoly_dict = result
#             else:
#                 polygon_list.append(result)
#         response[row.get("camera_no")] = {"polygon_list": polygon_list, "recPoly_dict": recPoly_dict}
#
#     print("successfully data loaded")
#     return response


def insert_events_db(camera_id, video_path, start_time, end_time):
    client = GetClientUpdateByComapnyCode()
    db = client["supervisorAI"]
    coll = db["productionData"]
    coll.insert_one({"cameraId": camera_id, "videoPath": video_path, "startTime": start_time, "endTime": end_time, "fileSize": -1})
    return True
