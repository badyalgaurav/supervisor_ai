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
    coll_logs = db["polygonLogs"]

    coll.update_one({"camera_no": camera_no},
                    {"$set": {"polygonInfo": [{"polygon": poly.get("transformedPoints"), "label": poly.get("name")} for poly in polygon_info], "camera_no": camera_no, "polyRawInfo": polygon_info,
                              "startTime": start_time, "endTime": end_time}}, upsert=True)
    coll_logs.insert_one({"polygonInfo": [{"polygon": poly.get("transformedPoints"), "label": poly.get("name")} for poly in polygon_info], "camera_no": camera_no, "polyRawInfo": polygon_info,
                          "startTime": start_time, "endTime": end_time, "createdDateTime": datetime.datetime.now()})
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
    start_date = datetime.datetime.strptime(datetime.datetime.now().date().strftime("%y-%m-%d %H:%M:%S"), '%y-%m-%d %H:%M:%S') - datetime.timedelta(days=3)
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

from logic.schemas.polygon_info_schemas import CameraInfo
def setup_registration(data: CameraInfo):
    client = GetClientUpdateByComapnyCode()
    db = client["supervisorAI"]
    coll = db["accountInfo"]
    d_dict=data.dict()
    parse_camera_info= json.loads(d_dict["cameraInfo"])
    d_dict["cameraInfo"]=parse_camera_info
    d_dict["isActive"]=True
    d_dict["createdDateTime"]=datetime.datetime.now()

    # //convert to dict(data)
    coll.insert_one(d_dict)
    return True


# import cv2
# import imutils
# from imutils.video import VideoStream
#
# rtsp_url = "rtsp://admin:Trace3@123@192.168.1.64:554/live"
#
#
# def main():
#     vs = VideoStream(rtsp_url).start()  # Open the RTSP stream
#     vs2 = VideoStream(rtsp_url).start()  # Open the RTSP stream
#     vs3 = VideoStream(rtsp_url).start()  # Open the RTSP stream
#     vs4 = VideoStream(rtsp_url).start()  # Open the RTSP stream
#
#     while True:
#
#         # Grab a frame at a time
#         frame = vs.read()
#         frame2 = vs2.read()
#         frame3 = vs3.read()
#         frame4 = vs4.read()
#         if frame is None:
#             continue
#
#         # Resize and display the frame on the screen
#         frame1 = imutils.resize(frame, width=812)
#         frame2 = imutils.resize(frame2, width=812)
#         frame3 = imutils.resize(frame3, width=812)
#         frame4 = imutils.resize(frame4, width=812)
#         cv2.imshow('WyzeCam', frame1)
#         cv2.imshow('WyzeCam2', frame2)
#         cv2.imshow('WyzeCam3', frame3)
#         cv2.imshow('WyzeCam4', frame4)
#
#         # Wait for the user to hit 'q' for quit
#         key = cv2.waitKey(1) & 0xFF
#         if key == ord('q'):
#             break
#
#     # Clean up and we're outta here.
#     cv2.destroyAllWindows()
#     vs.stop()
#
#
# if __name__ == "__main__":
#     main()