import datetime
import threading
import cv2
from ultralytics import YOLO
# import math
from logic.alarm import start_camera_alert, stop_camera_alert
from logic.mongo_op import insert_events_db

# import os
# model
model = YOLO("/logic/yolov8n.pt")
CONFIDENCE_THRESHOLD = 0.70
# object class logics
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
IS_PERSON_IN_DANGER = {1: False, 2: False, 3: False, 4: False}
IS_PERSON_REMAIN_IN_DANGER = {1: False, 2: False, 3: False, 4: False}
FRAME_H_BOX = {1: [], 2: [], 3: [], 4: []}
IS_PERSON_REMAIN_IN_DANGER_START_TIME = {1: "", 2: "", 3: "", 4: ""}

# Video recording variables
# Define a dictionary to store frame buffers for each camera
camera_frames = {1: [], 2: [], 3: [], 4: []}


def insert_event(camera_id, video_path, start_time, end_time):
    insert_events_db(camera_id, video_path, start_time, end_time)
    return "success"


# Function to record video in the danger zone
def record_video(camera_id, video_path):
    try:
        frames = camera_frames[camera_id]
        frame_height, frame_width, _ = frames[0].shape
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 format\
        fourcc = cv2.VideoWriter_fourcc(*'h264')
        out = cv2.VideoWriter(video_path, fourcc, 20, (frame_width, frame_height))
        for frame in frames:
            out.write(frame)
        out.release()
        camera_frames[camera_id] = []
        # Get the size of the video file
    except Exception as e:
        # Code to handle the exception (generic)
        print("An exception occurred:", e)
        out.release()
        camera_frames[camera_id] = []


def detect_yolo_person_in_polygon(camera_id, img, poly_info, danger_zone_poly):
    global IS_PERSON_IN_DANGER
    global IS_PERSON_REMAIN_IN_DANGER
    global IS_PERSON_REMAIN_IN_DANGER_START_TIME
    global camera_frames
    global FRAME_H_BOX

    results = model(img, stream=True, classes=0, conf=CONFIDENCE_THRESHOLD,imgsz=320)
    IS_PERSON_IN_DANGER[camera_id] = False
    # reset frame save
    FRAME_H_BOX[camera_id] = []

    for r in results:
        boxes = r.boxes
        FRAME_H_BOX[camera_id].append(boxes)
        draw_rect(camera_id, danger_zone_poly, poly_info, img, boxes)
    return img


def from_box_person_in_polygon(camera_id, img, poly_info, danger_zone_poly):
    try:
        if FRAME_H_BOX[camera_id]:
            for boxes in FRAME_H_BOX[camera_id]:
                draw_rect(camera_id,danger_zone_poly,poly_info,img, boxes)
    except Exception as e:
        print(f'{e}')
    return img


def draw_rect(camera_id,danger_zone_poly,poly_info,img,boxes):
    # frame_copied = img.copy()
    try:

        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            for i, polygon_points in enumerate(poly_info):
                # Check if any part of the person's bounding box intersects with the polygon
                if any(cv2.pointPolygonTest(polygon_points, (x1, y1), False) >= 0 for x1, y1 in [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]):
                    if i == danger_zone_poly:
                        IS_PERSON_IN_DANGER[camera_id] = True
                    # Draw bounding box and other details
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
                else:
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

        if IS_PERSON_IN_DANGER[camera_id]:
            # full if  block is for video recording
            if not IS_PERSON_REMAIN_IN_DANGER[camera_id]:
                IS_PERSON_REMAIN_IN_DANGER[camera_id] = True
                IS_PERSON_REMAIN_IN_DANGER_START_TIME[camera_id] = datetime.datetime.now()
                start_camera_alert(camera_id=camera_id)
            camera_frames[camera_id].append(img)

        else:
            # full if  block is for video recording
            if IS_PERSON_REMAIN_IN_DANGER[camera_id]:
                end_time = datetime.datetime.now()
                video_path = f"/var/www/camera_{camera_id}_{datetime.datetime.utcnow().microsecond}_video.mp4"
                recording_thread = threading.Thread(target=record_video, args=(camera_id, video_path))
                recording_thread.daemon = True
                recording_thread.start()
                insert_event(camera_id=camera_id, video_path=video_path,
                             start_time=IS_PERSON_REMAIN_IN_DANGER_START_TIME[camera_id], end_time=end_time)
                IS_PERSON_REMAIN_IN_DANGER[camera_id] = False
                IS_PERSON_REMAIN_IN_DANGER_START_TIME[camera_id] = ""
                stop_camera_alert(camera_id=camera_id)
                # print("no person not in danger zone")
    except:
        print("error")
    return img