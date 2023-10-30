import datetime
import threading
import cv2
from ultralytics import YOLO
import math
from logic.alarm import start_camera_alert, stop_camera_alert
from logic.mongo_op import insert_events_db
import os
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
IS_PERSON_IN_DANGER = {1: False, 2: False, 3: False, 4: False}
IS_PERSON_REMAIN_IN_DANGER = {1: False, 2: False, 3: False, 4: False}
IS_PERSON_REMAIN_IN_DANGER_START_TIME = {1: "", 2: "", 3: "", 4: ""}

# Video recording variables
# Define a dictionary to store frame buffers for each camera
camera_frames = {1: [], 2: [], 3: [], 4: []}


def insert_event(camera_id, video_path, start_time, end_time):
    insert_events_db(camera_id, video_path, start_time, end_time)
    return "success"


# Function to record video in the danger zone
def record_video(camera_id, video_path):
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

camera_ip = '192.168.1.64'
rtsp_port = '554'
username = 'admin'
password = 'Trace3@123'
url_rtsp = f'rtsp://{username}:{password}@{camera_ip}:{rtsp_port}'

def detect_yolo_person_in_polygon(camera_id, img, poly_info, danger_zone_poly):
    global IS_PERSON_IN_DANGER
    global IS_PERSON_REMAIN_IN_DANGER
    global IS_PERSON_REMAIN_IN_DANGER_START_TIME
    global camera_frames  # Assuming you have a global dictionary for frames
    frame_copied = img.copy()
    results = model(img, stream=True,classes=0)
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
                # print("Confidence --->", confidence)
                if confidence > CONFIDENCE_THRESHOLD:
                    # testing

                    for i, polygon_points in enumerate(poly_info):
                        # Check if any part of the person's bounding box intersects with the polygon
                        if any(cv2.pointPolygonTest(polygon_points, (x1, y1), False) >= 0 for x1, y1 in [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]):
                            if i == danger_zone_poly:
                                IS_PERSON_IN_DANGER[camera_id] = True
                            # Draw bounding box and other details
                            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
                            # org = [x1, y1]
                            # font = cv2.FONT_HERSHEY_SIMPLEX
                            # fontScale = 1
                            # color = (255, 0, 0)
                            # thickness = 2
                            # cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
                        else:
                            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                            # org = [x1, y1]
                            # font = cv2.FONT_HERSHEY_SIMPLEX
                            # fontScale = 1
                            # color = (255, 0, 0)
                            # thickness = 2
                            # cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

        if IS_PERSON_IN_DANGER[camera_id]:
            # full if  block is for video recording
            if not IS_PERSON_REMAIN_IN_DANGER[camera_id]:
                IS_PERSON_REMAIN_IN_DANGER[camera_id] = True
                IS_PERSON_REMAIN_IN_DANGER_START_TIME[camera_id] = datetime.datetime.now()

            camera_frames[camera_id].append(frame_copied)

            start_camera_alert(camera_id=camera_id)
        else:
            # full if  block is for video recording
            if IS_PERSON_REMAIN_IN_DANGER[camera_id]:
                end_time = datetime.datetime.now()
                video_path = f"/var/www/camera_{camera_id}_{datetime.datetime.utcnow().microsecond}_video.mp4"
                recording_thread = threading.Thread(target=record_video, args=(camera_id, video_path))
                recording_thread.daemon = True
                recording_thread.start()

                # # Wait for the thread to finish
                # recording_thread.join()
                #
                # # Retrieve the result from the queue
                # video_size = result_queue.get()


                insert_event(camera_id=camera_id, video_path=video_path,
                             start_time=IS_PERSON_REMAIN_IN_DANGER_START_TIME[camera_id], end_time=end_time)
                IS_PERSON_REMAIN_IN_DANGER[camera_id] = False
                IS_PERSON_REMAIN_IN_DANGER_START_TIME[camera_id] = ""

            stop_camera_alert(camera_id=camera_id)
            # print("no person not in danger zone")
    return img
