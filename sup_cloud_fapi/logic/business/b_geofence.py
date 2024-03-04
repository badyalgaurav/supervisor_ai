from typing import Optional
from dateutil import parser
from logic.utility import common
import pandas as pd
import json
import datetime
from shapely.geometry import Polygon


class Geofence:

    def __init__(self):
        self.client = common.get_mongo_client()

    def get_polygon(self, user_id: str):
        res = {"data": None, "message": "MSG_100"}
        db = self.client["UUAABBDD"]
        coll = db["polygonInfo"]
        df = pd.DataFrame(coll.find({"userId": user_id}, {"_id": 0})).to_json(orient="records")
        res["data"] = json.loads(df)
        return res

    def upsert_polygon(self, polygon_info: str, camera_no: int, start_time: Optional[str] = None, end_time: Optional[str] = None, user_id: Optional[str] = None):
        db = self.client["UUAABBDD"]
        coll = db["polygonInfo"]
        coll_logs = db["polygonLogs"]

        coll.update_one({"camera_no": camera_no, "userId": user_id},
                        {"$set": {"polygonInfo": [{"polygon": poly.get("transformedPoints"), "label": poly.get("name")} for poly in polygon_info], "camera_no": camera_no, "polyRawInfo": polygon_info,
                                  "startTime": start_time, "endTime": end_time, "userId": user_id}}, upsert=True)
        coll_logs.insert_one({"polygonInfo": [{"polygon": poly.get("transformedPoints"), "label": poly.get("name")} for poly in polygon_info], "camera_no": camera_no, "polyRawInfo": polygon_info,
                              "startTime": start_time, "endTime": end_time, "userId": user_id, "createdDateTime": datetime.datetime.now()})
        return True

    def get_time_data(self, user_id: str):
        res = {"data": None, "message": "MSG_100"}
        db = self.client["UUAABBDD"]
        coll = db["polygonInfo"]
        result = list(coll.find({"userId": user_id}, {"_id": 0, "startTime": 1, "endTime": 1, "camera_no": 1}))

        res["data"] = {i['camera_no']: {"startTime": i['startTime'], "endTime": i['endTime']} for i in result}
        return res

    def get_all_polygon(self, user_id: str):
        db = self.client["UUAABBDD"]
        coll = db["polygonInfo"]
        df = pd.DataFrame(coll.find({"userId": user_id}, {"_id": 0}))
        # Loop over the rows using iterrows()
        # response = {}

        # for index, row in df.iterrows():
        #     polygon_list = []
        #     rec_poly_dict = {}
        #     for polygon in row["polygonInfo"]:
        #         result = Polygon([(item['x'], item['y']) for item in polygon.get("polygon")])
        #         if polygon.get("label") == "recPoly":
        #             rec_poly_dict = result
        #         else:
        #             polygon_list.append(result)
        #     response[row.get("camera_no")] = {"polygon_list": polygon_list, "recPoly_dict": rec_poly_dict, "start_time": row.get("startTime"), "end_time": row.get("endTime")}
        res=json.loads(df.to_json(orient="records"))
        return res

    def insert_events_db(self, user_id: str, camera_id: int, video_path: str, start_time: str, end_time: str):
        db = self.client["UUAABBDD"]
        coll = db["productionData"]
        start_time = parser.parse(start_time)
        end_time = parser.parse(end_time)
        coll.insert_one({"userId": user_id, "cameraId": camera_id, "videoPath": video_path, "startTime": start_time, "endTime": end_time, "fileSize": -1})
        return True
