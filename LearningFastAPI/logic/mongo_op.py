from pymongo import MongoClient


def GetClientUpdateByComapnyCode():
    serverAddress = "127.0.0.1:2017"
    client = MongoClient(F"mongodb://{serverAddress}")
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
