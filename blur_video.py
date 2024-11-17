import cv2
import os
import tkinter as tk
from tkinter import messagebox
import moviepy.editor as mp

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
videos_dir = os.path.join(script_dir, 'videos')

# Make sure the 'videos' directory exists
if not os.path.exists(videos_dir):
    os.makedirs(videos_dir)

# Function to process the video
def process_video(input_name, output_name):
    # Default to looking in the 'videos' folder
    input_video = os.path.join(videos_dir, input_name)

    # Validate input file
    if not os.path.isfile(input_video):
        messagebox.showerror("Error", f"Input file '{input_name}' does not exist in the 'videos' folder.")
        return

    # Ensure the output video name ends with a valid extension
    if not output_name.endswith(('.mp4', '.mkv', '.avi')):
        output_name += ".mp4"

    # Check the output video path in the 'videos' folder
    output_video = os.path.join(videos_dir, output_name)

    try:
        # Open the input video using moviepy
        clip = mp.VideoFileClip(input_video)

        # Extract audio from the original video
        audio = clip.audio

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
        final_clip.write_videofile(output_video, codec="libx264", audio_codec="aac")

        messagebox.showinfo("Success", f"Video successfully saved to '{output_name}' in the 'videos' folder!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the Tkinter GUI
def create_gui():
    def on_process():
        input_name = input_entry.get().strip()
        output_name = output_entry.get().strip()
        
        if not input_name or not output_name:
            messagebox.showerror("Error", "Both input and output file names are required.")
        else:
            process_video(input_name, output_name)

    # Main Tkinter window
    root = tk.Tk()
    root.title("Blur Video Processor")

    # Input file label and entry
    tk.Label(root, text="Input File Name (e.g., input_video.mp4):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    input_entry = tk.Entry(root, width=40)
    input_entry.grid(row=0, column=1, padx=10, pady=5)

    # Output file label and entry
    tk.Label(root, text="Output File Name (e.g., output_video.mp4):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    output_entry = tk.Entry(root, width=40)
    output_entry.grid(row=1, column=1, padx=10, pady=5)

    # Default extension label
    tk.Label(root, text="* If no extension is provided, '.mp4' will be used by default.", fg="gray").grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    # Process button
    process_button = tk.Button(root, text="Process Video", command=on_process)
    process_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Start the Tkinter event loop
    root.mainloop()

# Run the GUI
create_gui()
