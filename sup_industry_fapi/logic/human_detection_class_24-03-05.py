import datetime

import cv2
import os
from ultralytics import YOLO
import time

from shapely.geometry import box as box_shape

from logic.alarm import start_camera_alert, stop_camera_alert
from logic.mongo_op import insert_events_db

# from geofence.alarm import start_camera_alert, stop_camera_alert
# from geofence.mongo_op import insert_events_db
# export the model to ONNX format
# yolo_model.export(format='onnx')
yolo_model = YOLO("yolov8n.pt")


confidence_threshold = 0.60


def is_current_time_in_range(start_time, end_time):
    current_datetime = datetime.datetime.now()
    start_time = datetime.datetime.strptime(start_time, "%H:%M")
    end_time = datetime.datetime.strptime(end_time, "%H:%M")
    start_datetime = current_datetime.replace(hour=start_time.hour, minute=start_time.minute, second=0, microsecond=0)
    end_datetime = current_datetime.replace(hour=end_time.hour, minute=end_time.minute, second=0, microsecond=0)

    return start_datetime <= current_datetime <= end_datetime


class CameraProcessor:
    def __init__(self, user_id,camera_id):

        self.start_time = None
        self.duration_per_file = 60 * 1  # 1 minutes in seconds
        self.user_id=user_id
        self.camera_id = camera_id
        self.model = yolo_model

        # Polygon and camera state initialization
        self.is_person_in_danger = False
        # self.is_alert = False
        self.is_person_in_warning = False
        self.is_person_remain_in_warning = False
        self.is_person_remain_in_danger = False
        self.person_state = 0  # 0: Not in danger zone, 1: In danger zone

        # Video recording variables
        # self.camera_frames = []
        self.frame_h_boxes = []
        self.is_person_remain_in_danger_start_time = ""
        self.video_filename = self.generate_file_name()
        self.video_writer = None

    def detect_person_in_polygon(self, img, poly_info, rec_poly_info, config_options: dict):
        results = self.model(img, stream=True, classes=[0], conf=confidence_threshold, imgsz=320)

        self.is_person_in_danger = False
        self.frame_h_boxes = []
        try:
            for r in results:
                # if r.boxes.id is not None:
                if len(r.boxes.xyxy.cpu()):
                    boxes = r.boxes.xyxy.cpu()
                    self.frame_h_boxes.append(boxes)
        except:
            pass

        if self.frame_h_boxes:
            self.draw_rect(img, poly_info, rec_poly_info, config_options)
        else:
            stop_camera_alert(self.camera_id)

        return img

    def from_box_person_in_polygon(self, img, poly_info, rec_poly_info, config_options: dict):
        try:
            if self.frame_h_boxes:
                # for boxes in self.frame_h_boxes:
                self.draw_rect(img, poly_info, rec_poly_info, config_options)
        except Exception as e:
            print(f'{e}')
        return img

    def draw_rect(self, img, poly_info, rec_poly_info, config_options: dict):
        for boxes in self.frame_h_boxes:
            for box in boxes:
                x1, y1, x2, y2 = box
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # warning zone
                if box_shape(x1, y1, x2, y2).intersects(rec_poly_info):
                    self.is_person_in_warning = True
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 3)
                else:
                    # safe zone
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

                # danger zone
                for i, polygon_points in enumerate(poly_info):
                    if box_shape(x1, y1, x2, y2).intersects(polygon_points):
                        # if polygon_points.contains(Point((bbox_center[0], bbox_center[1]))):
                        self.is_person_in_danger = True
                        self.is_person_in_warning = True
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
        self.process_frame(config_options)
        return img

    def process_frame(self, config_options: dict):
        if is_current_time_in_range(config_options.get("start_time"), config_options.get("end_time")):
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
        insert_events_db(self.user_id,self.camera_id, video_path, start_time, end_time)
        return "success"

    # def write_frame_to_disk_async(self, frame):
    #     current_time = time.time()
    #
    #     # this if condition code is only for generating new file for video recording and saving current file + save the data to db if anytime within the range intrusion occured.
    #     if self.start_time is None or (current_time - self.start_time) >= self.duration_per_file:
    #
    #         self.start_time = current_time
    #         if self.is_person_in_warning:
    #             start_save_time = datetime.datetime.now() - datetime.timedelta(seconds=self.duration_per_file)
    #             end_save_time = datetime.datetime.now()
    #             self.insert_event(self.video_filename, start_save_time, end_save_time)
    #             self.is_person_in_warning = False
    #
    #     if self.video_writer is not None and self.video_writer.isOpened():
    #         self.video_writer.write(frame)
    #     else:
    #         # Release the previous video writer asynchronously
    #         self.release_video_writer()
    #         # generate new filename and video writer
    #         self.video_filename = self.generate_file_name()
    #         self.video_writer = self.generate_video_writer(frame)

    def write_frame_to_disk_async(self, frame):
        current_time = time.time()
        # this if condition code is only for generating new file for video recording and saving current file + save the data to db if anytime within the range intrusion occured.
        if self.start_time is None or current_time - self.start_time >= self.duration_per_file:
            # if self.video_writer.isOpened():  # Check if VideoWriter is open
            if self.is_person_in_warning:
                start_save_time = datetime.datetime.now() - datetime.timedelta(seconds=self.duration_per_file)
                end_save_time = datetime.datetime.now()
                self.insert_event(self.video_filename, start_save_time, end_save_time)
                self.is_person_in_warning = False

            if self.video_writer is not None:
                self.video_writer.release()
                self.video_filename = self.generate_file_name()

            self.video_writer = self.generate_video_writer(frame=frame)
            self.start_time = current_time

        if self.video_writer is not None and self.video_writer.isOpened():
            self.video_writer.write(frame)

    def generate_file_name(self):
        current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        current_date = datetime.datetime.now().strftime("%Y%m%d")
        output_folder = f"/var/www/output_camera_{self.camera_id}/{current_date}"
        os.makedirs(output_folder, exist_ok=True)
        video_filename = f"{output_folder}/output_camera_{self.camera_id}_{current_datetime}.mp4"
        return video_filename

    def generate_video_writer(self, frame):
        frame_height, frame_width, _ = frame.shape
        fourcc = cv2.VideoWriter_fourcc(*'h264')
        # fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # cv2.VideoWriter_fourcc(*'h264')
        # fourcc = cv2.VideoWriter_fourcc(*"MJPG")  # cv2.VideoWriter_fourcc(*'h264')
        # fourcc = cv2.VideoWriter_fourcc(*"avc1")  # cv2.VideoWriter_fourcc(*'h264')
        fps = 15
        frame_size = (frame_width, frame_height)
        video_writer = cv2.VideoWriter(self.video_filename, fourcc, fps, frame_size)
        return video_writer

    # def release_video_writer(self):
    #     asyncio.create_task(self.release_video_writer_async())
    #
    # async def release_video_writer_async(self):
    #     if self.video_writer is not None:
    #         self.video_writer.release()
    #         self.video_writer = None
    # def release_video_writer(self):
    #     if self.video_writer is not None:
    #         self.video_writer.release()
    #         self.video_writer = None
