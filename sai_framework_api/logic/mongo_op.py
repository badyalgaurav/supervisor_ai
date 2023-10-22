from pymongo import MongoClient
import datetime
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


def get_alert_counts():
    res = {"data": None, "message": "MSG_100"}
    client = GetClientUpdateByComapnyCode()
    db = client["supervisorAI"]
    coll = db["productionData"]
    start_date = datetime.datetime.strptime(datetime.datetime.now().date().strftime("%y-%m-%d %H:%M:%S"), '%y-%m-%d %H:%M:%S')
    end_date = start_date + datetime.timedelta(days=1)
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
        },{"$project":{
            '_id': 0,  # Exclude the _id field
            'cameraId': '$_id',  # Rename _id to cameraId
            'count': 1  # Include the count field
        }}
    ]
    # df = pd.DataFrame(coll.find({'TimeStamp': {'$lt': end_date, '$gte': start_date}}, {"_id": 0,"cameraId":1})).to_json(orient="records")
    result = list(coll.aggregate(pipeline))
    res["data"] = {i['cameraId']: i['count'] for i in result}
    return res



