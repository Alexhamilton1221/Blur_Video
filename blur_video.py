import cv2
import os

def get_valid_video_filename():
    while True:
        input_video = input("Enter the name of the input video file (e.g., input_video.mp4): ")
        if os.path.isfile(input_video):
            cap = cv2.VideoCapture(input_video)
            if cap.isOpened():
                cap.release()
                return input_video
            else:
                print(f"Error: The file '{input_video}' cannot be opened as a video. Please try again.")
        else:
            print(f"Error: The file '{input_video}' does not exist. Please try again.")

input_video = get_valid_video_filename()
output_video = input("Enter the name of the output video file (e.g., output_video.mp4): ")
if not output_video.endswith(('.mp4', '.mkv', '.avi')):
    output_video += ".mp4"
    print(f"Defaulting output file name to: {output_video}")

cap = cv2.VideoCapture(input_video)

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"Video Properties - FPS: {fps}, Width: {width}, Height: {height}")

if fps == 0 or width == 0 or height == 0:
    print("Error: Failed to retrieve video properties. Check input video.")
    exit()

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

blur_duration_frames = 20 * fps  # 20 seconds in frames
no_blur_duration_frames = 20 * fps  # 20 seconds in frames

frame_index = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print(f"End of video reached or error reading frame at index {frame_index}")
        break

    # Check if the frame should be blurred
    # Alternate: First 20 seconds unblurred, next 20 seconds blurred
    if (frame_index // blur_duration_frames) % 2 == 1:
        frame = cv2.GaussianBlur(frame, (51, 51), 0)

    # Write to output and display for debugging
    out.write(frame)
    cv2.imshow('Processing Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_index += 1

cap.release()
out.release()
cv2.destroyAllWindows()
