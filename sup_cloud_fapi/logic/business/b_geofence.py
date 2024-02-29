from typing import Optional

from logic.utility import common
import pandas as pd
import json
import datetime


class Geofence:

    def __init__(self):
        self.client = common.get_mongo_client()

    def get_polygon(self):
        res = {"data": None, "message": "MSG_100"}
        db = self.client["supervisorAI"]
        coll = db["polygonInfo"]
        df = pd.DataFrame(coll.find({}, {"_id": 0})).to_json(orient="records")
        res["data"] = json.loads(df)
        return res

    def upsert_polygon(self, polygon_info: str, camera_no: int, start_time: Optional[str] = None, end_time: Optional[str] = None):
        db = self.client["supervisorAI"]
        coll = db["polygonInfo"]
        coll_logs = db["polygonLogs"]

        coll.update_one({"camera_no": camera_no},
                        {"$set": {"polygonInfo": [{"polygon": poly.get("transformedPoints"), "label": poly.get("name")} for poly in polygon_info], "camera_no": camera_no, "polyRawInfo": polygon_info,
                                  "startTime": start_time, "endTime": end_time}}, upsert=True)
        coll_logs.insert_one({"polygonInfo": [{"polygon": poly.get("transformedPoints"), "label": poly.get("name")} for poly in polygon_info], "camera_no": camera_no, "polyRawInfo": polygon_info,
                              "startTime": start_time, "endTime": end_time, "createdDateTime": datetime.datetime.now()})
        return True

    def get_time_data(self):
        res = {"data": None, "message": "MSG_100"}
        db = self.client["supervisorAI"]
        coll = db["polygonInfo"]
        result = list(coll.find({}, {"_id": 0, "startTime": 1, "endTime": 1, "camera_no": 1}))

        res["data"] = {i['camera_no']: {"startTime": i['startTime'], "endTime": i['endTime']} for i in result}
        return res
