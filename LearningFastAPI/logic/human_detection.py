import cv2
import numpy as np
from ultralytics import YOLO
import math
# model
model = YOLO("/logic/yolov8n.pt")

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
#full classes detection
def detect_yolo(img):
    results = model(img, stream=True)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confidence
            confidence = math.ceil((box.conf[0] * 100)) / 100
            print("Confidence --->", confidence)

            # class name
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
    return img

#only human  detection
def detect_yolo_person_only(img):
    results = model(img, stream=True)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # class name
            cls = int(box.cls[0])

            # Check if the detected class is "person"
            if classNames[cls] == "person":
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # put box in cam
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100
                print("Confidence --->", confidence)

                # object details
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2

                cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
    return img


def detect_yolo_person_in_boundary(img, boundary_x1, boundary_y1, boundary_x2, boundary_y2):
    results = model(img, stream=True)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # class name
            cls = int(box.cls[0])

            # Check if the detected class is "person"
            if classNames[cls] == "person":
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                # default boundry check
                # cv2.rectangle(img, (boundary_x1, boundary_y1), (boundary_x2, boundary_y2), (255, 0, 0), 3)
                # Define the vertices of the polygon
                polygon_points = np.array([(100, 100), (200, 100), (200, 200), (100, 200)], dtype=np.int32)
                polygon_points = polygon_points.reshape((-1, 1, 2))
                cv2.polylines(img,[polygon_points], isClosed=True, color= (255, 255, 0), thickness=4)
                # Check if the person bounding box is inside the boundary rectangle
                # if boundary_x1 <= x1 or boundary_y1 <= y1 or boundary_x2 >= x2 or boundary_y2 >= y2:
                # Check if any part of the person's bounding box intersects with the boundary rectangle
                if x1 < boundary_x2 and x2 > boundary_x1 and y1 < boundary_y2 and y2 > boundary_y1:
                    # Draw bounding box and other details
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
                    confidence = math.ceil((box.conf[0] * 100)) / 100
                    print("Confidence --->", confidence)
                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 2
                    cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
                else:
                    # Draw bounding box and other details
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    confidence = math.ceil((box.conf[0] * 100)) / 100
                    print("Confidence --->", confidence)
                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    color = (0, 255, 0)
                    thickness = 2
                    cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
    return img

#polygon
def detect_yolo_person_in_polygon(img):
    results = model(img, stream=True)
    # Define the vertices of the polygon
    polygon_points = np.array([(100, 100), (200, 100), (200, 200), (100, 200)], dtype=np.int32)
    polygon_points = polygon_points.reshape((-1, 1, 2))
    # Iterate through the detected objects
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

                # Check if any part of the person's bounding box intersects with the polygon
                if all(cv2.pointPolygonTest(polygon_points, (x1, y1), False) >= 0 for x1, y1 in [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]):
                    # Draw bounding box and other details
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
                    confidence = math.ceil((box.conf[0] * 100)) / 100
                    print("Confidence --->", confidence)
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

    # Draw the polygon on the image
    cv2.polylines(img, [polygon_points], isClosed=True, color=(255, 255, 0), thickness=4)

    return img