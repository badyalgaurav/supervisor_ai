import os
import cv2


def generate_images_from_videos(video_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the video folder
    for filename in os.listdir(video_folder):
        filepath = os.path.join(video_folder, filename)

        # Check if the file is a video
        if os.path.isfile(filepath) and filename.endswith(('.mp4', '.avi', '.mkv')):
            # Open the video file
            cap = cv2.VideoCapture(filepath)

            # Read the video frame by frame
            success, frame = cap.read()
            frame_count = 0

            while success:
                # Generate filename for the image
                image_filename = f"{os.path.splitext(filename)[0]}_{frame_count}.jpg"
                output_filepath = os.path.join(output_folder, image_filename)

                # Write the frame as an image
                cv2.imwrite(output_filepath, frame)

                # Read the next frame
                success, frame = cap.read()
                frame_count += 1

            # Release the video capture object
            cap.release()


if __name__ == "__main__":
    # Specify the input folder containing videos
    video_folder = "D:\\chthaShotlifter"

    # Specify the output folder to save generated images
    output_folder = "D:\\chthaShotlifter\\images"

    # Generate images from videos in the input folder
    generate_images_from_videos(video_folder, output_folder)
