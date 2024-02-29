import datetime
from logic.schemas.camera_schemas import CameraInfo
from logic.utility import common
import json


class Gemmiz:

    def __init__(self):
        self.client = common.get_mongo_client()

    def setup_registration(self, data: CameraInfo):
        db = self.client["UUAABBDD"]
        coll = db["accountInfo"]
        d_dict = data.dict()
        parse_camera_info = json.loads(d_dict["cameraInfo"])
        d_dict["cameraInfo"] = parse_camera_info
        d_dict["isActive"] = True
        d_dict["createdDateTime"] = datetime.datetime.now()
        coll.insert_one(d_dict)
        return True

    def get_camera_credentials(self, email: str, password: str):
        db = self.client["UUAABBDD"]
        coll = db["accountInfo"]
        response = coll.find_one({"cEmail": email, "cPassword": password, "isActive": True})
        response["_id"]=str(response["_id"])
        return response
