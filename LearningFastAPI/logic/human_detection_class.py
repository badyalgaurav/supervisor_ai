
##########################RnD##############################################
import datetime
import threading
import cv2
from ultralytics import YOLO
from logic.alarm import start_camera_alert, stop_camera_alert
from logic.mongo_op import insert_events_db
yolo_model = YOLO("/logic/yolov8n.pt")
class_names = ["person"]  # (list of class names)
confidence_threshold = 0.60
class CameraProcessor:
    def __init__(self, camera_id):
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

# Example usage
# camera_processor_1 = CameraProcessor(camera_id=1)
# camera_processor_2 = CameraProcessor(camera_id=2)

# Call these methods as needed
# camera_processor_1.detect_person_in_polygon(...)
# camera_processor_1.draw_rect(...)
# camera_processor_2.detect_person_in_polygon(...)
# camera_processor_2.draw_rect(...)
