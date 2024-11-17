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

# Function to process video with user-defined box
def process_video(input_video, output_video, no_blur_duration, blur_duration, x1, y1, x2, y2, time_intervals=None):
    try:
        # Process video frames
        cap = cv2.VideoCapture(input_video)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        # Remove temp file if it already exists
        temp_output_video = os.path.join(videos_dir, "temp_output.mp4")
        if os.path.exists(temp_output_video):
            os.remove(temp_output_video)
        
        out = cv2.VideoWriter(temp_output_video, fourcc, fps, (width, height))

        frame_index = 0
        interval_index = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print(f"End of video reached or error reading frame at index {frame_index}")
                break

            if time_intervals:  # Use time intervals mode
                if interval_index < len(time_intervals):
                    # Check if it's time to apply blur for the current interval
                    if time_intervals[interval_index][0] <= frame_index / fps < time_intervals[interval_index][1]:
                        blurred_frame = cv2.GaussianBlur(frame, (51, 51), 0)
                        blurred_frame[y1:y2, x1:x2] = frame[y1:y2, x1:x2]
                        frame = blurred_frame
                    frame_index += 1
                    # Move to next interval if the current one is finished
                    if frame_index / fps >= time_intervals[interval_index][1]:
                        interval_index += 1
                else:
                    # No more intervals, stop applying blur
                    frame_index += 1
            else:  # Use blur cycles mode
                if (frame_index // blur_duration) % 2 == 1:
                    blurred_frame = cv2.GaussianBlur(frame, (51, 51), 0)
                    blurred_frame[y1:y2, x1:x2] = frame[y1:y2, x1:x2]
                    frame = blurred_frame
                frame_index += 1

            out.write(frame)

        cap.release()
        out.release()

        # After video is processed, ensure we add audio
        original_clip = mp.VideoFileClip(input_video)
        processed_clip = mp.VideoFileClip(temp_output_video)
        final_clip = processed_clip.set_audio(original_clip.audio)
        final_clip.write_videofile(output_video, codec="libx264", audio_codec="aac")

        # Cleanup the temporary output video after it's been used
        os.remove(temp_output_video)
        print("Processing complete.")
        messagebox.showinfo("Success", f"Video processed successfully!\nSaved at: {output_video}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    try:
        # Process video frames
        cap = cv2.VideoCapture(input_video)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        temp_output_video = os.path.join(videos_dir, "temp_output.mp4")
        out = cv2.VideoWriter(temp_output_video, fourcc, fps, (width, height))

        frame_index = 0
        interval_index = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print(f"End of video reached or error reading frame at index {frame_index}")
                break

            if time_intervals:  # Use time intervals mode
                # Check if interval_index is within bounds
                if interval_index < len(time_intervals):
                    # Check if it's time to apply blur for the current interval
                    if time_intervals[interval_index][0] <= frame_index / fps < time_intervals[interval_index][1]:
                        blurred_frame = cv2.GaussianBlur(frame, (51, 51), 0)
                        blurred_frame[y1:y2, x1:x2] = frame[y1:y2, x1:x2]
                        frame = blurred_frame
                    frame_index += 1
                    # If we've passed the end of the current interval, move to the next one
                    if frame_index / fps >= time_intervals[interval_index][1]:
                        interval_index += 1
                else:
                    # No more intervals, we just process the rest of the video without any blur
                    frame_index += 1
            else:  # Use blur cycles mode
                # If we're in the blurring phase
                if (frame_index // blur_duration) % 2 == 1:
                    blurred_frame = cv2.GaussianBlur(frame, (51, 51), 0)
                    blurred_frame[y1:y2, x1:x2] = frame[y1:y2, x1:x2]
                    frame = blurred_frame
                frame_index += 1

            out.write(frame)

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
    try:
        # Process video frames
        cap = cv2.VideoCapture(input_video)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        temp_output_video = os.path.join(videos_dir, "temp_output.mp4")
        out = cv2.VideoWriter(temp_output_video, fourcc, fps, (width, height))

        frame_index = 0
        interval_index = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print(f"End of video reached or error reading frame at index {frame_index}")
                break

            if time_intervals:  # Use time intervals mode
                # Check if it's time to apply blur
                if time_intervals[interval_index][0] <= frame_index / fps < time_intervals[interval_index][1]:
                    blurred_frame = cv2.GaussianBlur(frame, (51, 51), 0)
                    blurred_frame[y1:y2, x1:x2] = frame[y1:y2, x1:x2]
                    frame = blurred_frame
                frame_index += 1
                if frame_index / fps >= time_intervals[interval_index][1]:
                    interval_index += 1
            else:  # Use blur cycles mode
                # If we're in the blurring phase
                if (frame_index // blur_duration) % 2 == 1:
                    blurred_frame = cv2.GaussianBlur(frame, (51, 51), 0)
                    blurred_frame[y1:y2, x1:x2] = frame[y1:y2, x1:x2]
                    frame = blurred_frame
                frame_index += 1

            out.write(frame)

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

    def toggle_mode():
        if mode_var.get() == 1:  # Using time intervals
            blur_duration_label.grid_forget()
            no_blur_duration_label.grid_forget()
            blur_duration_spin.grid_forget()
            no_blur_duration_spin.grid_forget()
            time_intervals_box.grid(row=6, column=1, padx=10, pady=10)
        else:  # Using blur cycles
            time_intervals_box.grid_forget()
            blur_duration_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
            no_blur_duration_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
            blur_duration_spin.grid(row=5, column=1, padx=10, pady=10)
            no_blur_duration_spin.grid(row=4, column=1, padx=10, pady=10)

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
        elif not output_name.endswith(('.mp4', '.mkv', '.avi')):  # Ensuring correct file extension
            output_name += ".mp4"

        output_video = os.path.join(output_folder, output_name)

        try:
            no_blur_duration = int(no_blur_duration_var.get())
            blur_duration = int(blur_duration_var.get())
            x1, y1, x2, y2 = int(x1_var.get()), int(y1_var.get()), int(x2_var.get()), int(y2_var.get())

            time_intervals = None
            if mode_var.get() == 1:  # Time intervals mode
                time_intervals_str = time_intervals_var.get()
                try:
                    # Parse the time intervals input
                    time_intervals = []
                    intervals = time_intervals_str.split(",")
                    for interval in intervals:
                        start, end = interval.split("-")
                        time_intervals.append((int(start), int(end)))
                except ValueError:
                    messagebox.showerror("Error", "Invalid time intervals format. Please enter time ranges like '10-15,15-30'.")
                    return

            process_video(input_video, output_video, no_blur_duration, blur_duration, x1, y1, x2, y2, time_intervals)
        except ValueError:
            messagebox.showerror("Error", "Invalid values entered. Please enter valid numbers.")

    window = tk.Tk()
    window.title("Video Blurring Tool")
    window.geometry("600x500")  # Increased window size to fit all components

    # Input Video File
    Label(window, text="Input Video File:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    input_file_var = tk.StringVar()
    Entry(window, textvariable=input_file_var, width=40).grid(row=0, column=1, padx=10, pady=10)
    Button(window, text="Browse", command=select_input_file).grid(row=0, column=2, padx=10, pady=10)

    # Output Folder
    Label(window, text="Output Folder:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    output_folder_var = tk.StringVar(value=videos_dir)
    Entry(window, textvariable=output_folder_var, width=40).grid(row=1, column=1, padx=10, pady=10)
    Button(window, text="Browse", command=select_output_folder).grid(row=1, column=2, padx=10, pady=10)

    # Output Video Name
    Label(window, text="Output Video File Name:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    output_file_var = tk.StringVar()
    Entry(window, textvariable=output_file_var, width=40).grid(row=2, column=1, padx=10, pady=10)

    Label(window, text="Default output extension: .mp4").grid(row=3, column=1, padx=10, pady=5)

    # Mode selection
    mode_var = tk.IntVar(value=0)  # 0 for blur cycles, 1 for time intervals
    Label(window, text="Select Mode:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
    tk.Radiobutton(window, text="Blur Cycles", variable=mode_var, value=0, command=toggle_mode).grid(row=4, column=1)
    tk.Radiobutton(window, text="Time Intervals", variable=mode_var, value=1, command=toggle_mode).grid(row=4, column=2)

    # Time interval settings
    time_intervals_label = Label(window, text="Time Intervals (comma-separated seconds):")
    time_intervals_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
    time_intervals_var = tk.StringVar()
    time_intervals_box = Entry(window, textvariable=time_intervals_var, width=40)

    # Blur Duration (for blur cycles mode)
    blur_duration_label = Label(window, text="Blur Duration (seconds):")
    blur_duration_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
    blur_duration_var = tk.StringVar(value="5")
    blur_duration_spin = Spinbox(window, from_=1, to=60, textvariable=blur_duration_var)
    blur_duration_spin.grid(row=5, column=1, padx=10, pady=10)

    # Non-Blur Duration (for blur cycles mode)
    no_blur_duration_label = Label(window, text="Non-Blur Duration (seconds):")
    no_blur_duration_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
    no_blur_duration_var = tk.StringVar(value="10")
    no_blur_duration_spin = Spinbox(window, from_=1, to=60, textvariable=no_blur_duration_var)
    no_blur_duration_spin.grid(row=6, column=1, padx=10, pady=10)

    # Coordinates
    Label(window, text="Coordinates (x1, y1, x2, y2):").grid(row=7, column=0, padx=10, pady=10, sticky="w")
    x1_var = tk.StringVar(value="0")
    y1_var = tk.StringVar(value="0")
    x2_var = tk.StringVar(value="100")
    y2_var = tk.StringVar(value="100")
    Entry(window, textvariable=x1_var, width=10).grid(row=7, column=1, padx=10, pady=10)
    Entry(window, textvariable=y1_var, width=10).grid(row=7, column=2, padx=10, pady=10)
    Entry(window, textvariable=x2_var, width=10).grid(row=7, column=3, padx=10, pady=10)
    Entry(window, textvariable=y2_var, width=10).grid(row=7, column=4, padx=10, pady=10)

    # Start Processing Button
    Button(window, text="Start Processing", command=process_video_with_gui).grid(row=8, column=0, columnspan=3, padx=10, pady=20)

    window.mainloop()

# Run the GUI
start_gui()
