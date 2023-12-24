##########################RnD##############################################
import asyncio
import datetime
import threading
import cv2
import numpy as np
from ultralytics import YOLO
from logic.alarm import start_camera_alert, stop_camera_alert
from logic.mongo_op import insert_events_db

yolo_model = YOLO("/logic/yolov8n.pt")
class_names = ["person"]  # (list of class names)
confidence_threshold = 0.60


class CameraProcessor:
    def __init__(self, camera_id):
        self.video_writer = None
        self.start_time = None
        self.duration_per_file = 300  # 5 minutes in seconds


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
        self.is_person_in_warning = False
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
        # frame_copied = img.copy()

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
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

        self.process_frame(img)

        return img

    def process_frame(self, frame):
        if self.is_person_in_danger:
            self.handle_person_in_danger()
        else:
            self.handle_person_not_in_danger()

        if self.is_person_in_warning:
            self.handle_person_in_warning(frame)
        else:
            self.handle_person_not_in_warning(frame)

    def handle_person_in_danger(self):
        if self.person_state == 0:
            start_camera_alert(camera_id=self.camera_id)
            self.person_state = 1  # Update state to indicate person is in danger zone

    def handle_person_not_in_danger(self):
        if self.person_state == 1:
            stop_camera_alert(camera_id=self.camera_id)
            self.person_state = 0  # Update state to indicate person is not in danger zone

    def handle_person_in_warning(self, frame):
        if not self.is_person_remain_in_danger:
            self.is_person_remain_in_danger = True
            self.is_person_remain_in_danger_start_time = datetime.datetime.now()

        self.camera_frames.append(frame.copy())

    def handle_person_not_in_warning(self, frame):
        if self.is_person_remain_in_danger:
            end_time = datetime.datetime.now()
            video_path = f"/var/www/camera_{self.camera_id}_{datetime.datetime.utcnow().microsecond}_video.mp4"
            recording_thread = threading.Thread(target=self.record_video, args=(video_path,))
            recording_thread.daemon = True
            recording_thread.start()
            self.insert_event(video_path, end_time)
            self.is_person_remain_in_danger = False
            self.is_person_remain_in_danger_start_time = ""

    def record_video(self, video_path):
        try:
            frames = self.camera_frames
            if frames:
                frame_height, frame_width, _ = frames[0].shape
                fourcc = cv2.VideoWriter_fourcc(*'h264')
                out = cv2.VideoWriter(video_path, fourcc, 20, (frame_width, frame_height))

                for frame in frames:
                    out.write(frame)

                out.release()
                self.camera_frames = []
        except Exception as e:
            print("An exception occurred:", e)

    def insert_event(self, video_path, end_time):
        insert_events_db(self.camera_id, video_path, self.is_person_remain_in_danger_start_time, end_time)
        return "success"

    async def write_frame_to_disk(self, frame):
        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        # Asynchronously write the frame to disk
        await asyncio.to_thread(self._write_frame_to_disk_async, frame_bytes)

    def _write_frame_to_disk_async(self, frame_bytes):
        # Check if a new video file needs to be created
        current_time = datetime.time.time()
        if self.start_time is None or current_time - self.start_time >= self.duration_per_file:
            # Close the existing VideoWriter if it exists
            if self.video_writer is not None:
                self.video_writer.release()

            # Create a new video file
            current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            video_filename = f"output_camera_{self.camera_id}_{current_datetime}.avi"
            fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Adjust codec as needed
            fps = 25  # Adjust frames per second as needed
            frame_size = (640, 480)  # Adjust frame size as needed

            self.video_writer = cv2.VideoWriter(video_filename, fourcc, fps, frame_size)
            self.start_time = current_time

        # Convert frame_bytes back to a frame
        frame = cv2.imdecode(np.frombuffer(frame_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)

        # Write the frame to the video file
        self.video_writer.write(frame)

    def release_video_writer(self):
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None
