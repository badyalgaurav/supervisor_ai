from pymongo import MongoClient
import pandas as pd

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

def get_all_polygon():
    client = GetClientUpdateByComapnyCode()
    db = client["supervisorAI"]
    coll = db["polygonInfo"]
    df=pd.DataFrame(coll.find({}, {"_id": 0}))
    # Loop over the rows using iterrows()
    response = {}

    for index, row in df.iterrows():
        polygon_list = []
        for polygon in row["polygonInfo"]:
            result = [(item['x'], item['y']) for item in polygon.get("polygon")]
            polygon_list.append(result)
            print(f"{polygon}")

        response[row.get("camera_no")]=polygon_list


    return response