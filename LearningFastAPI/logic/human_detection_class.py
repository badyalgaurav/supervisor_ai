import datetime
import cv2
import os
from ultralytics import YOLO
from logic.alarm import start_camera_alert, stop_camera_alert
from logic.mongo_op import insert_events_db
import time

yolo_model = YOLO("/logic/yolov8n.pt")
class_names = ["person"]  # (list of class names)
confidence_threshold = 0.60


class CameraProcessor:
    def __init__(self, camera_id):
        self.video_writer = None
        self.start_time = None
        self.duration_per_file = 60  # 1 minutes in seconds

        self.camera_id = camera_id
        self.model = yolo_model

        # Polygon and camera state initialization
        self.is_person_in_danger = False
        self.is_person_in_warning = False
        self.is_person_remain_in_warning = False
        self.is_person_remain_in_danger = False
        self.person_state = 0  # 0: Not in danger zone, 1: In danger zone

        # Video recording variables
        self.camera_frames = []
        self.frame_h_boxes = []
        self.is_person_remain_in_danger_start_time = ""

    def detect_person_in_polygon(self, img, poly_info, rec_poly_info):
        results = self.model(img, stream=True, classes=0, conf=confidence_threshold, imgsz=320)
        self.is_person_in_danger = False
        # self.is_person_in_warning = False
        self.frame_h_boxes = []

        for r in results:
            boxes = r.boxes
            self.frame_h_boxes.append(boxes)
        self.draw_rect(img, poly_info, rec_poly_info)
        return img

    def from_box_person_in_polygon(self, img, poly_info, rec_poly_info):
        try:
            if self.frame_h_boxes:
                # for boxes in self.frame_h_boxes:
                self.draw_rect(img, poly_info, rec_poly_info)
        except Exception as e:
            print(f'{e}')
        return img

    def draw_rect(self, img, poly_info, rec_poly_info):
        for boxes in self.frame_h_boxes:
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                if any(cv2.pointPolygonTest(rec_poly_info, (x1, y1), False) >= 0 for x1, y1 in [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]):
                    self.is_person_in_warning = True
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 3)
                else:
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

                for i, polygon_points in enumerate(poly_info):
                    if any(cv2.pointPolygonTest(polygon_points, (x1, y1), False) >= 0 for x1, y1 in [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]):
                        self.is_person_in_danger = True
                        self.is_person_in_warning = True
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

        self.process_frame(img)

        return img

    def process_frame(self, frame):
        if self.is_person_in_danger:
            self.handle_person_in_danger()
        else:
            self.handle_person_not_in_danger()

    def handle_person_in_danger(self):
        if self.person_state == 0:
            start_camera_alert(camera_id=self.camera_id)
            self.person_state = 1  # Update state to indicate person is in danger zone

    def handle_person_not_in_danger(self):
        if self.person_state == 1:
            stop_camera_alert(camera_id=self.camera_id)
            self.person_state = 0  # Update state to indicate person is not in danger zone

    def insert_event(self, video_path, start_time, end_time):
        insert_events_db(self.camera_id, video_path, start_time, end_time)
        return "success"

    def write_frame_to_disk_async(self, frame):
        current_time = time.time()
        video_filename = self.create_file_name()

        if self.start_time is None or current_time - self.start_time >= self.duration_per_file:
            frame_height, frame_width, _ = frame.shape
            # fourcc = cv2.VideoWriter_fourcc(*'h264')
            fourcc = cv2.VideoWriter_fourcc(*'h264')
            fps = 15
            frame_size = (frame_width, frame_height)

            if self.video_writer is not None:
                self.video_writer.release()

            self.video_writer = cv2.VideoWriter(video_filename, fourcc, fps, frame_size)
            self.start_time = current_time

            if self.video_writer.isOpened():  # Check if VideoWriter is open
                if self.is_person_in_warning:
                    start_save_time = datetime.datetime.now() - datetime.timedelta(seconds=self.duration_per_file)
                    end_save_time = datetime.datetime.now()
                    self.insert_event(video_filename, start_save_time, end_save_time)
                    self.is_person_in_warning = False

        if self.video_writer is not None and self.video_writer.isOpened():
            self.video_writer.write(frame)

    def create_file_name(self):
        current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        # Create a folder for the current date if it doesn't exist
        current_date = datetime.datetime.now().strftime("%Y%m%d")
        output_folder = f"/var/www/output_camera_{self.camera_id}/{current_date}"
        os.makedirs(output_folder, exist_ok=True)
        video_filename = f"{output_folder}/output_camera_{self.camera_id}_{current_datetime}.mp4"
        return video_filename

    def release_video_writer(self):
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None
