import datetime

import cv2
from ultralytics import YOLO
import math
from logic.alarm import start_camera_alert, stop_camera_alert
from logic.mongo_op import insert_events_db
# model
model = YOLO("/logic/yolov8n.pt")
CONFIDENCE_THRESHOLD = 0.70
# object classlogic/es
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

# polygon
IS_PERSON_IN_DANGER = {1:False,2:False,3:False,4:False}
IS_PERSON_REMAIN_IN_DANGER = {1:False,2:False,3:False,4:False}
IS_PERSON_REMAIN_IN_DANGER_START_TIME = {1:"",2:"",3:"",4:""}

def insert_event(camera_id,video_path,start_time, end_time):
    insert_events_db(camera_id, video_path,start_time,end_time)
    return "success"

def detect_yolo_person_in_polygon(camera_id,img, poly_info,danger_zone_poly):
    global IS_PERSON_IN_DANGER
    global IS_PERSON_REMAIN_IN_DANGER
    global IS_PERSON_REMAIN_IN_DANGER_START_TIME
    results = model(img, stream=True)
    # Define the vertices of the polygon
    # polygon_points = np.array([(100, 100), (200, 100), (200, 500), (100, 500)], dtype=np.int32)
    # if poly_info:
    #     polygon_points = np.array(poly_info[1], dtype=np.int32)
    # polygon_points = polygon_points.reshape((-1, 1, 2))
    # Iterate through the detected objects
    IS_PERSON_IN_DANGER[camera_id] = False
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Class index
            cls = int(box.cls[0])

            # Check if the detected class is "person"
            if classNames[cls] == "person":
                # Bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                confidence = math.ceil((box.conf[0] * 100)) / 100
                print("Confidence --->", confidence)
                if confidence > CONFIDENCE_THRESHOLD:
                    for i, polygon_points in enumerate(poly_info):
                        # Check if any part of the person's bounding box intersects with the polygon
                        if any(cv2.pointPolygonTest(polygon_points, (x1, y1), False) >= 0 for x1, y1 in [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]):
                            if i==danger_zone_poly:
                                IS_PERSON_IN_DANGER[camera_id]  = True
                                if IS_PERSON_REMAIN_IN_DANGER[camera_id] ==False:
                                    IS_PERSON_REMAIN_IN_DANGER[camera_id] =True
                                    IS_PERSON_REMAIN_IN_DANGER_START_TIME[camera_id] =datetime.datetime.now()

                            # Draw bounding box and other details
                            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
                            org = [x1, y1]
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            fontScale = 1
                            color = (255, 0, 0)
                            thickness = 2
                            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

                        else:
                            if IS_PERSON_REMAIN_IN_DANGER[camera_id] :
                                end_time=datetime.datetime.now()
                                insert_event(camera_id=camera_id,video_path="video_path",start_time=IS_PERSON_REMAIN_IN_DANGER_START_TIME[camera_id] ,
                                             end_time=end_time)
                                IS_PERSON_REMAIN_IN_DANGER[camera_id] =False
                                IS_PERSON_REMAIN_IN_DANGER_START_TIME[camera_id] =""
                            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                            org = [x1, y1]
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            fontScale = 1
                            color = (255, 0, 0)
                            thickness = 2
                            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

        if IS_PERSON_IN_DANGER[camera_id]:
            start_camera_alert(camera_id=camera_id)
        else:
            stop_camera_alert(camera_id=camera_id)
            print("no person not in danger zone")

    # Draw the polygon on the image\
    # Convert the list of lists to a NumPy array
    # my_array = np.array(json.loads(poly_points), dtype=np.int32)
    # cv2.polylines(img, [polygon_points], isClosed=True, color=(255, 255, 0), thickness=4)

    return img
