import cv2
from onvif import ONVIFCamera
import numpy as np
from ultralytics import YOLO
import math
from logic.alarm import start_danger_alert,stop_danger_alert
# model
model = YOLO("/logic/yolov8n.pt")
CONFIDENCE_THRESHOLD=0.70
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

#polygon
IS_PERSON_IN_DANGER=False
def detect_yolo_person_in_polygon(img):
    global IS_PERSON_IN_DANGER
    results = model(img, stream=True)
    # Define the vertices of the polygon
    polygon_points = np.array([(100, 100), (200, 100), (200, 500), (100, 500)], dtype=np.int32)
    polygon_points = polygon_points.reshape((-1, 1, 2))
    # Iterate through the detected objects
    IS_PERSON_IN_DANGER = False
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
                    # Check if any part of the person's bounding box intersects with the polygon
                    if any(cv2.pointPolygonTest(polygon_points, (x1, y1), False) >= 0 for x1, y1 in [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]):
                        print("person in danger zone")
                        IS_PERSON_IN_DANGER=True

                        # Draw bounding box and other details
                        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 3)


                        org = [x1, y1]
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        fontScale = 1
                        color = (255, 0, 0)
                        thickness = 2
                        cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
                    else:


                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                        confidence = math.ceil((box.conf[0] * 100)) / 100
                        print("Confidence --->", confidence)
                        org = [x1, y1]
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        fontScale = 1
                        color = (255, 0, 0)
                        thickness = 2
                        cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

        if IS_PERSON_IN_DANGER:
            start_danger_alert()
        else:
            stop_danger_alert()
            print("no person not in danger zone")

    # Draw the polygon on the image
    # cv2.polylines(img, [polygon_points], isClosed=True, color=(255, 255, 0), thickness=4)

    return img