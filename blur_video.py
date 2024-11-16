import cv2
import os
import moviepy.editor as mp

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
videos_dir = os.path.join(script_dir, 'videos')

# Make sure the 'videos' directory exists
if not os.path.exists(videos_dir):
    os.makedirs(videos_dir)

def get_valid_video_filename():
    while True:
        input_video = input(f"Enter the name of the input video file (e.g., input_video.mp4) from the '{videos_dir}' folder: ")
        
        # Default to looking in the 'videos' folder
        video_path = os.path.join(videos_dir, input_video)
        
        if os.path.isfile(video_path):
            cap = cv2.VideoCapture(video_path)
            if cap.isOpened():
                cap.release()
                return video_path
            else:
                print(f"Error: The file '{input_video}' cannot be opened as a video. Please try again.")
        else:
            print(f"Error: The file '{input_video}' does not exist in the 'videos' folder. Please try again.")

input_video = get_valid_video_filename()

# Get the output file name
output_video = input("Enter the name of the output video file (e.g., output_video.mp4): ")

# Ensure the output video name ends with a valid extension
if not output_video.endswith(('.mp4', '.mkv', '.avi')):
    output_video += ".mp4"
    print(f"Defaulting output file name to: {output_video}")

# Check the output video path in the 'videos' folder
output_video_path = os.path.join(videos_dir, output_video)

# Open the input video using moviepy
clip = mp.VideoFileClip(input_video)

# Extract audio from the original video
audio = clip.audio

# Get video properties
fps = clip.fps
width, height = clip.size
print(f"Video Properties - FPS: {fps}, Width: {width}, Height: {height}")

# Apply blur effect to the video
def apply_blur(get_frame, t):
    frame = get_frame(t)  # Get frame at time t
    blur_duration = 20  # blur every 20 seconds alternately
    if int(t) // blur_duration % 2 == 1:  # Apply blur every 20 seconds alternately
        frame = cv2.GaussianBlur(frame, (51, 51), 0)
    return frame

# Create the processed video clip with blur effect applied
blurred_clip = clip.fl(apply_blur, keep_duration=True)

# Write the final video with the blurred video and original audio
final_clip = blurred_clip.set_audio(audio)
final_clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

print(f"Video with audio saved to {output_video_path}")
