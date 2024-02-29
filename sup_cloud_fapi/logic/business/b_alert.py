import datetime
import pandas as pd
from dateutil import parser
from logic.utility import common
import json


class Alert:

    def __init__(self):
        self.client = common.get_mongo_client()

    def get_alert_counts(self):
        res = {"data": None, "message": "MSG_100"}
        db = self.client["supervisorAI"]
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
            }, {"$project": {
                '_id': 0,  # Exclude the _id field
                'cameraId': '$_id',  # Rename _id to cameraId
                'count': 1  # Include the count field
            }}
        ]
        result = list(coll.aggregate(pipeline))
        res["data"] = {i['cameraId']: i['count'] for i in result}
        return res

    def get_alert_details(self, camera_id: int, start_date: str, end_date: str):
        start_date = parser.parse(start_date)
        end_date = parser.parse(end_date)
        res = {"data": None, "message": "MSG_100"}
        db = self.client["supervisorAI"]
        coll = db["productionData"]
        if start_date == end_date:
            end_date = start_date + datetime.timedelta(days=1)

        df = pd.DataFrame(list(coll.find({'startTime': {'$lt': end_date, '$gte': start_date}, "cameraId": camera_id}, {"_id": 0})))
        df = df.applymap(str)
        res["data"] = json.loads(df.to_json(orient="records"))
        return res
