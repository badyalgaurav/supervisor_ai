from imutils.video import VideoStream
import imutils
import asyncio
import cv2
import time
import concurrent.futures
from logic.human_detection_class import CameraProcessor
# from logic.retail_detection_class import CameraProcessor
from logic.mongo_op import get_all_polygon


# from geofence.human_detection_class import CameraProcessor
# from geofence.mongo_op import get_all_polygon


class FrameGenerator:
    def __init__(self, user_id, camera_id, url_rtsp, height, width, ai_per_second):
        # to get the database info periodically
        self.database_data = {}
        asyncio.create_task(self.fetch_data_periodically())
        self.thread_pool = concurrent.futures.ThreadPoolExecutor()
        self.camera_id = camera_id
        self.user_id = user_id
        self.camera_processor = CameraProcessor(user_id, camera_id)
        self.url_rtsp = f'{url_rtsp}' if "rtsp" in url_rtsp else int(url_rtsp)
        try:
            self.camera_streams = VideoStream(0).start()
            if self.camera_streams.grabbed:
                print("SUCCESS: successfully initialized")
            else:
                print("WARNING: please check the camera connection. For testing you can use VLC player's IP Camera player option.")
        except Exception as e:
            print("ERROR:", e)

        self.frame_counters = 0
        self.height = int(height)
        self.width = int(width)
        self.ai_per_second = ai_per_second if ai_per_second else 10

        # Create a dictionary to store thread termination flags
        self.thread_termination_flags = False
        self.display_frame = None

    async def fetch_data_periodically(self):
        while True:
            # Retrieve data from the database
            new_data = get_all_polygon(self.user_id)  # Replace with your actual query
            # Update the instance variable with the new data
            self.database_data = new_data
            # Sleep for 5 minutes before checking again
            await asyncio.sleep(30)  # 300 seconds = 5 minutes

    async def generate_frames(self):
        try:
            # camera_processor = CameraProcessor(self.camera_id)
            restart_stream = False
            while not self.thread_termination_flags:
                frame = self.camera_streams.read()
                if frame is not None:
                    frame = imutils.resize(frame, width=self.width, height=self.height)
                    # copy_frame = frame.copy()
                    # write video file
                    await asyncio.to_thread(self.camera_processor.write_frame_to_disk_async, frame)
                    self.frame_counters += 1
                    if self.database_data:
                        poly_info = self.database_data.get(self.camera_id).get("polygon_list")
                        rec_poly_info = self.database_data.get(self.camera_id).get("recPoly_dict")
                        start_time = self.database_data.get(self.camera_id).get("start_time")
                        end_time = self.database_data.get(self.camera_id).get("end_time")
                        config_options = {"start_time": start_time, "end_time": end_time}
                        # 5
                        if self.frame_counters % self.ai_per_second == 0:
                            # await asyncio.to_thread(self.camera_processor.detect_person_in_polygon, frame, poly_info, rec_poly_info,config_options)
                            # Use a thread pool for CPU-bound tasks
                            loop = asyncio.get_running_loop()
                            await loop.run_in_executor(
                                self.thread_pool,
                                self.camera_processor.detect_person_in_polygon,
                                frame, poly_info, rec_poly_info, config_options
                            )
                            self.frame_counters = 0
                        else:
                            await asyncio.to_thread(self.camera_processor.from_box_person_in_polygon, frame, poly_info, rec_poly_info, config_options)

                    _, buffer = cv2.imencode(".jpg", frame)
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n' b'Content-Type: image/jpg\r\n\r\n' + frame_bytes + b'\r\n')
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
        # finally:
        #     await asyncio.to_thread(self.camera_processor.release_video_writer)
        #     self.camera_streams.stream.release()

    async def generate_frames_bg(self):
        try:
            restart_stream = False
            while not self.thread_termination_flags:
                frame = self.camera_streams.read()
                if frame is not None:
                    frame = imutils.resize(frame, width=self.width, height=self.height)
                    await asyncio.to_thread(self.camera_processor.write_frame_to_disk_async, frame)
                    self.frame_counters += 1
                    if self.database_data:
                        poly_info = self.database_data.get(self.camera_id).get("polygon_list")
                        rec_poly_info = self.database_data.get(self.camera_id).get("recPoly_dict")
                        start_time = self.database_data.get(self.camera_id).get("start_time")
                        end_time = self.database_data.get(self.camera_id).get("end_time")
                        config_options = {"start_time": start_time, "end_time": end_time}
                        if self.frame_counters % self.ai_per_second == 0:
                            loop = asyncio.get_running_loop()
                            await loop.run_in_executor(
                                self.thread_pool,
                                self.camera_processor.detect_person_in_polygon,
                                frame, poly_info, rec_poly_info, config_options
                            )
                            self.frame_counters = 0
                        else:
                            await asyncio.to_thread(self.camera_processor.from_box_person_in_polygon, frame, poly_info, rec_poly_info, config_options)

                    self.display_frame = frame
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
        # finally:
        #     await asyncio.to_thread(self.camera_processor.release_video_writer)
        #     self.camera_streams.stream.release()
