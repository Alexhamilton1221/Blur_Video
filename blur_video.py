import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Label, Entry, Button, Spinbox
import moviepy.editor as mp

# Get the directory of the current script and default to a 'videos' folder
script_dir = os.path.dirname(os.path.abspath(__file__))
videos_dir = os.path.join(script_dir, 'videos')
if not os.path.exists(videos_dir):
    os.makedirs(videos_dir)

# Function to get exclusion zone coordinates
def get_exclusion_zone():
    # Example coordinates for an exclusion zone
    # Top-left corner (x1, y1), Bottom-right corner (x2, y2)
    return 50, 50, 250, 250  # Modify these values as needed

# Function to process video with audio
def process_video(input_video, output_video, no_blur_duration, blur_duration):
    try:
        # Define the exclusion zone
        exclusion_zone = get_exclusion_zone()
        x1, y1, x2, y2 = exclusion_zone

        # Process video frames
        cap = cv2.VideoCapture(input_video)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        temp_output_video = os.path.join(videos_dir, "temp_output.mp4")
        out = cv2.VideoWriter(temp_output_video, fourcc, fps, (width, height))

        no_blur_frames = no_blur_duration * fps
        blur_frames = blur_duration * fps
        frame_index = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                print(f"End of video reached or error reading frame at index {frame_index}")
                break

            # If we're in the blurring phase
            if (frame_index // blur_frames) % 2 == 1:
                blurred_frame = cv2.GaussianBlur(frame, (51, 51), 0)
                blurred_frame[y1:y2, x1:x2] = frame[y1:y2, x1:x2]
                frame = blurred_frame

            out.write(frame)
            frame_index += 1

        cap.release()
        out.release()

        # Add audio to the processed video
        original_clip = mp.VideoFileClip(input_video)
        processed_clip = mp.VideoFileClip(temp_output_video)
        final_clip = processed_clip.set_audio(original_clip.audio)
        final_clip.write_videofile(output_video, codec="libx264", audio_codec="aac")

        # Cleanup temporary file
        os.remove(temp_output_video)
        print("Processing complete.")
        messagebox.showinfo("Success", f"Video processed successfully!\nSaved at: {output_video}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# GUI Application
def start_gui():
    def select_input_file():
        input_path = filedialog.askopenfilename(initialdir=videos_dir, title="Select Input Video File",
                                                filetypes=(("Video Files", "*.mp4 *.mkv *.avi"), ("All Files", "*.*")))
        if input_path:
            input_file_var.set(input_path)

    def select_output_folder():
        output_path = filedialog.askdirectory(initialdir=videos_dir, title="Select Output Folder")
        if output_path:
            output_folder_var.set(output_path)

    def process_video_with_gui():
        input_video = input_file_var.get()
        output_folder = output_folder_var.get()
        output_name = output_file_var.get()

        if not input_video:
            messagebox.showerror("Error", "Please select an input video file.")
            return

        if not os.path.isfile(input_video):
            messagebox.showerror("Error", "The input video file does not exist.")
            return

        if not output_name.strip():
            output_name = "output_video.mp4"
        elif not output_name.endswith(('.mp4', '.mkv', '.avi')):
            output_name += ".mp4"

        output_video = os.path.join(output_folder, output_name)

        try:
            no_blur_duration = int(no_blur_duration_var.get())
            blur_duration = int(blur_duration_var.get())
            process_video(input_video, output_video, no_blur_duration, blur_duration)
        except ValueError:
            messagebox.showerror("Error", "Invalid duration values. Please enter valid numbers.")

    window = tk.Tk()
    window.title("Video Blurring Tool")
    window.geometry("500x300")

    Label(window, text="Input Video File:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    input_file_var = tk.StringVar()
    Entry(window, textvariable=input_file_var, width=40).grid(row=0, column=1, padx=10, pady=10)
    Button(window, text="Browse", command=select_input_file).grid(row=0, column=2, padx=10, pady=10)

    Label(window, text="Output Folder:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    output_folder_var = tk.StringVar(value=videos_dir)
    Entry(window, textvariable=output_folder_var, width=40).grid(row=1, column=1, padx=10, pady=10)
    Button(window, text="Browse", command=select_output_folder).grid(row=1, column=2, padx=10, pady=10)

    Label(window, text="Output Video File Name:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    output_file_var = tk.StringVar()
    Entry(window, textvariable=output_file_var, width=40).grid(row=2, column=1, padx=10, pady=10)

    Label(window, text="Default output extension: .mp4").grid(row=3, column=1, padx=10, pady=5)

    Label(window, text="Non-blur Duration (seconds):").grid(row=4, column=0, padx=10, pady=10, sticky="w")
    no_blur_duration_var = tk.StringVar(value="20")
    Spinbox(window, from_=1, to=60, textvariable=no_blur_duration_var).grid(row=4, column=1, padx=10, pady=10)

    Label(window, text="Blur Duration (seconds):").grid(row=5, column=0, padx=10, pady=10, sticky="w")
    blur_duration_var = tk.StringVar(value="20")
    Spinbox(window, from_=1, to=60, textvariable=blur_duration_var).grid(row=5, column=1, padx=10, pady=10)

    Button(window, text="Process Video", command=process_video_with_gui).grid(row=6, column=1, pady=20)

    window.mainloop()

if __name__ == "__main__":
    start_gui()
