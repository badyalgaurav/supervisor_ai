from pymongo import MongoClient
import pandas as pd
import json
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


def get_polygon():
    res = {"data": None, "message": "MSG_100"}
    client = GetClientUpdateByComapnyCode()
    db = client["supervisorAI"]
    coll = db["polygonInfo"]
    df = pd.DataFrame(coll.find({}, {"_id": 0})).to_json(orient="records")
    res["data"] = json.loads(df)
    return res
