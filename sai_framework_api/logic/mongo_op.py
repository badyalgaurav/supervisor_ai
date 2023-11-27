from pymongo import MongoClient
import datetime
import pandas as pd
import json
from dateutil import parser
from typing import Optional


def GetClientUpdateByComapnyCode():
    serverAddress = "127.0.0.1:27017"
    client = MongoClient(f"mongodb://{serverAddress}")
    return client


def upsert_polygon(polygon_info: str, camera_no: int, start_time: Optional[str] = None, end_time: Optional[str] = None):
    client = GetClientUpdateByComapnyCode()
    db = client["supervisorAI"]
    coll = db["polygonInfo"]

    # to add the top and left with y and x points
    # for poly in polygon_info:
    #     for points in poly.get("points"):
    #         points["x"]=poly.get("left")+points.get("x")
    #         points["y"]=poly.get("top")+points.get("y")

    coll.update_one({"camera_no": camera_no},
                    {"$set": {"polygonInfo": [{"polygon": poly.get("transformedPoints"), "label": poly.get("name")} for poly in polygon_info], "camera_no": camera_no, "polyRawInfo": polygon_info,
                              "startTime": start_time, "endTime": end_time}}, upsert=True)
    return True


def get_polygon():
    res = {"data": None, "message": "MSG_100"}
    client = GetClientUpdateByComapnyCode()
    db = client["supervisorAI"]
    coll = db["polygonInfo"]
    df = pd.DataFrame(coll.find({}, {"_id": 0})).to_json(orient="records")
    res["data"] = json.loads(df)
    return res


def get_alert_counts():
    res = {"data": None, "message": "MSG_100"}
    client = GetClientUpdateByComapnyCode()
    db = client["supervisorAI"]
    coll = db["productionData"]
    start_date = datetime.datetime.strptime(datetime.datetime.now().date().strftime("%y-%m-%d %H:%M:%S"), '%y-%m-%d %H:%M:%S')- datetime.timedelta(days=3)
    end_date = start_date + datetime.timedelta(days=5)
    # Perform the aggregation
    pipeline = [
        {
            '$match': {
                'startTime': {'$lt': end_date, '$gte': start_date}
            }
        },
        {
            '$group': {
                '_id': '$cameraId',
                'count': {'$sum': 1}
            }
        }, {"$project": {
            '_id': 0,  # Exclude the _id field
            'cameraId': '$_id',  # Rename _id to cameraId
            'count': 1  # Include the count field
        }}
    ]
    # df = pd.DataFrame(coll.find({'TimeStamp': {'$lt': end_date, '$gte': start_date}}, {"_id": 0,"cameraId":1})).to_json(orient="records")
    result = list(coll.aggregate(pipeline))
    res["data"] = {i['cameraId']: i['count'] for i in result}
    return res


def get_alert_details(camera_id: int, start_date: str, end_date: str):
    start_date = parser.parse(start_date)
    end_date = parser.parse(end_date)
    res = {"data": None, "message": "MSG_100"}
    client = GetClientUpdateByComapnyCode()
    db = client["supervisorAI"]
    coll = db["productionData"]
    # start_date = datetime.datetime.strptime(datetime.datetime.now().date().strftime("%y-%m-%d %H:%M:%S"), '%y-%m-%d %H:%M:%S')
    if start_date == end_date:
        end_date = start_date + datetime.timedelta(days=1)

    df = pd.DataFrame(list(coll.find({'startTime': {'$lt': end_date, '$gte': start_date}, "cameraId": camera_id}, {"_id": 0})))
    df = df.applymap(str)
    res["data"] = json.loads(df.to_json(orient="records"))
    return res


def get_time_data():
    res = {"data": None, "message": "MSG_100"}
    client = GetClientUpdateByComapnyCode()
    db = client["supervisorAI"]
    coll = db["polygonInfo"]
    result = list(coll.find({}, {"_id": 0, "startTime": 1, "endTime": 1, "camera_no": 1}))

    res["data"] = {i['camera_no']: {"startTime": i['startTime'], "endTime": i['endTime']} for i in result}
    return res
