from logic.human_detection_class import CameraProcessor
from imutils.video import VideoStream
import imutils
import asyncio
import cv2
import time
from logic.mongo_op import get_all_polygon

# Define a global variable to store the data
database_data = None


async def fetch_data_periodically():
    while True:
        # Retrieve data from the database
        new_data = get_all_polygon()  # Replace with your actual query
        # Update the global data with the new data
        global database_data
        database_data = new_data
        # Sleep for 5 minutes before checking again
        await asyncio.sleep(120)  # 300 seconds = 5 minutes


class FrameGenerator:
    def __init__(self, camera_id, url_rtsp, height, width):
        # to get the database info periodically
        asyncio.create_task(fetch_data_periodically())

        self.camera_id = camera_id
        self.camera_processor = CameraProcessor(camera_id)
        self.url_rtsp = f'{url_rtsp}'
        self.camera_streams = VideoStream(self.url_rtsp).start()
        self.frame_counters = 0
        self.height = int(height)
        self.width = int(width)

        # Create a dictionary to store thread termination flags
        self.thread_termination_flags = False

    async def generate_frames(self):
        try:
            restart_stream = False
            while not self.thread_termination_flags:
                frame = self.camera_streams.read()
                if frame is not None:
                    frame = imutils.resize(frame, width=self.width, height=self.height)
                    copy_frame = frame.copy()
                    self.frame_counters += 1
                    poly_info = database_data.get(self.camera_id).get("polygon_list")
                    rec_poly_info = database_data.get(self.camera_id).get("recPoly_dict")

                    if self.frame_counters % 10 == 0:
                        await asyncio.to_thread(self.camera_processor.detect_person_in_polygon, frame, poly_info, rec_poly_info)
                        self.frame_counters = 0
                    else:
                        await asyncio.to_thread(self.camera_processor.from_box_person_in_polygon, frame, poly_info, rec_poly_info)

                    _, buffer = cv2.imencode(".jpg", frame)
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                    self.camera_processor.write_frame_to_disk_async(copy_frame)
                else:
                    # Set the flag to restart the stream
                    restart_stream = True

                if restart_stream:
                    # Stop the current stream
                    self.camera_streams.stop()
                    self.camera_streams.stream.release()
                    # Introduce a delay before reinitializing
                    time.sleep(10)
                    # Reinitialize the video stream
                    self.camera_streams = VideoStream(self.url_rtsp).start()
                    # Reset the restart flag
                    restart_stream = False

        except Exception as e:
            print(f"Exception: {e}")
            # Optionally, print the traceback
            import traceback
            traceback.print_exc()
            pass
        finally:
            await asyncio.to_thread(self.camera_processor.release_video_writer)
            self.camera_streams.stream.release()
