import cv2
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import moviepy.editor as mp

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
videos_dir = os.path.join(script_dir, 'videos')

# Ensure the 'videos' directory exists
if not os.path.exists(videos_dir):
    os.makedirs(videos_dir)

# Function to process the video
def process_video(input_path, output_name, non_blur_duration, blur_duration, output_dir):
    if not os.path.isfile(input_path):
        messagebox.showerror("Error", f"The input file does not exist: {input_path}")
        return

    # Use default output name if none is provided
    if not output_name.strip():
        output_name = "output_video.mp4"

    # Ensure the output video name has a valid extension
    if not output_name.endswith(('.mp4', '.mkv', '.avi')):
        output_name += ".mp4"

    # Construct full output video path
    output_video = os.path.join(output_dir, output_name)

    try:
        # Open the input video using moviepy
        clip = mp.VideoFileClip(input_path)

        # Extract audio from the original video
        audio = clip.audio

        # Apply blur effect to the video
        def apply_blur(get_frame, t):
            frame = get_frame(t)  # Get frame at time t
            total_duration = non_blur_duration + blur_duration
            if int(t) % total_duration >= non_blur_duration:  # Apply blur after the non-blur period
                frame = cv2.GaussianBlur(frame, (51, 51), 0)
            return frame

        # Create the processed video clip with blur effect applied
        blurred_clip = clip.fl(apply_blur, keep_duration=True)

        # Write the final video with the blurred video and original audio
        final_clip = blurred_clip.set_audio(audio)
        final_clip.write_videofile(output_video, codec="libx264", audio_codec="aac")

        messagebox.showinfo("Success", f"Video successfully saved to '{output_video}'!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the Tkinter GUI
def create_gui():
    def on_process():
        input_path = input_file_var.get().strip()
        output_name = output_entry.get().strip()
        non_blur_duration = int(non_blur_spinner.get())
        blur_duration = int(blur_spinner.get())
        output_dir = output_dir_var.get()

        if not input_path:
            messagebox.showerror("Error", "Input video file is required.")
        else:
            process_video(input_path, output_name, non_blur_duration, blur_duration, output_dir)

    def select_input_file():
        input_path = filedialog.askopenfilename(initialdir=videos_dir, title="Select Input Video File",
                                                filetypes=[("Video Files", "*.mp4 *.mkv *.avi")])
        if input_path:
            input_file_var.set(input_path)

    def select_output_dir():
        selected_dir = filedialog.askdirectory(initialdir=videos_dir, title="Select Output Directory")
        if selected_dir:
            output_dir_var.set(selected_dir)

    # Main Tkinter window
    root = tk.Tk()
    root.title("Blur Video Processor")

    # Input file selection
    tk.Label(root, text="Input Video File:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    input_file_var = tk.StringVar()
    input_file_entry = tk.Entry(root, textvariable=input_file_var, width=40, state="readonly")
    input_file_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    input_file_button = tk.Button(root, text="Browse", command=select_input_file)
    input_file_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")

    # Output file label and entry
    tk.Label(root, text="Output File Name (Default: output_video.mp4):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    output_entry = tk.Entry(root, width=40)
    output_entry.grid(row=1, column=1, padx=10, pady=5)

    # Output directory label and selection
    tk.Label(root, text="Output Directory:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    output_dir_var = tk.StringVar(value=videos_dir)
    output_dir_entry = tk.Entry(root, textvariable=output_dir_var, width=40, state="readonly")
    output_dir_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    output_dir_button = tk.Button(root, text="Browse", command=select_output_dir)
    output_dir_button.grid(row=2, column=2, padx=10, pady=5, sticky="w")

    # Non-blur duration label and spinner
    tk.Label(root, text="Non-Blur Period (seconds):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    non_blur_spinner = ttk.Spinbox(root, from_=1, to=60, width=5)
    non_blur_spinner.set(20)  # Default value
    non_blur_spinner.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Blur duration label and spinner
    tk.Label(root, text="Blur Period (seconds):").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    blur_spinner = ttk.Spinbox(root, from_=1, to=60, width=5)
    blur_spinner.set(20)  # Default value
    blur_spinner.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    # Process button
    process_button = tk.Button(root, text="Process Video", command=on_process)
    process_button.grid(row=5, column=0, columnspan=3, pady=10)

    # Start the Tkinter event loop
    root.mainloop()

# Run the GUI
create_gui()
