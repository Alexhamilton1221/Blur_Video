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
                    # Apply blur everywhere except during the specified intervals
                    if not (time_intervals[interval_index][0] <= frame_index / fps < time_intervals[interval_index][1]):
                        blurred_frame = cv2.GaussianBlur(frame, (51, 51), 0)
                        blurred_frame[y1:y2, x1:x2] = frame[y1:y2, x1:x2]
                        frame = blurred_frame
                    frame_index += 1
                    # Move to next interval if the current one is finished
                    if frame_index / fps >= time_intervals[interval_index][1]:
                        interval_index += 1
                else:
                    # Apply blur for the rest of the video after all intervals
                    blurred_frame = cv2.GaussianBlur(frame, (51, 51), 0)
                    blurred_frame[y1:y2, x1:x2] = frame[y1:y2, x1:x2]
                    frame = blurred_frame
                    frame_index += 1
            else:  # Use blur cycles mode
                def apply_blur_logic(frame, t):
                    total_duration = no_blur_duration + blur_duration
                    if int(t) % total_duration >= no_blur_duration:  # Apply blur after no-blur period
                        blurred_frame = cv2.GaussianBlur(frame, (51, 51), 0)
                        blurred_frame[y1:y2, x1:x2] = frame[y1:y2, x1:x2]
                        return blurred_frame
                    return frame

                frame_time = frame_index / fps  # Calculate current time
                frame = apply_blur_logic(frame, frame_time)
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
  
# GUI Application
def start_gui():
    def select_input_file():
        input_path = filedialog.askopenfilename(initialdir=videos_dir, title="Select Input Video File",
                                                filetypes=(("Video Files", "*.mp4 *.mkv *.avi"), ("All Files", "*.*")))
        if input_path:
            input_file_var.set(input_path)
            # Get video dimensions after selecting file
            cap = cv2.VideoCapture(input_path)
            global width, height  # Declare globally so it can be used in Spinbox max values
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()
            # Update the Spinboxes with the new video dimensions
            x1_entry.config(to=width)
            y1_entry.config(to=height)
            x2_entry.config(to=width)
            y2_entry.config(to=height)

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
    window.geometry("800x500")  # Increased window size to fit all components

    # Initialize default video dimensions
    global width, height
    width = 640  # Default width
    height = 480  # Default height

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
    output_file_var = tk.StringVar(value="output_video.mp4")
    Entry(window, textvariable=output_file_var, width=40).grid(row=2, column=1, padx=10, pady=10)

    # Mode (Blur Cycles / Time Intervals)
    mode_var = tk.IntVar(value=0)
    Label(window, text="Choose Mode:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
    tk.Radiobutton(window, text="Blur Cycles", variable=mode_var, value=0, command=toggle_mode).grid(row=3, column=1)
    tk.Radiobutton(window, text="Time Intervals", variable=mode_var, value=1, command=toggle_mode).grid(row=3, column=2)

    # Time Intervals Box
    Label(window, text="Time Intervals (e.g., 10-20,30-40) seconds for unblur:").grid(row=6, column=0, padx=10, pady=10, sticky="w")
    time_intervals_var = tk.StringVar()
    time_intervals_box = Entry(window, textvariable=time_intervals_var, width=40)

    # Blur Duration settings
    blur_duration_label = Label(window, text="Blur Duration (seconds):")
    blur_duration_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
    blur_duration_var = tk.IntVar(value=5)
    blur_duration_spin = Spinbox(window, from_=1, to=30, textvariable=blur_duration_var, width=10)

    # No Blur Duration settings
    no_blur_duration_label = Label(window, text="No Blur Duration (seconds):")
    no_blur_duration_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    no_blur_duration_var = tk.IntVar(value=5)
    no_blur_duration_spin = Spinbox(window, from_=1, to=30, textvariable=no_blur_duration_var, width=10)

    # Coordinates for blur area
    Label(window, text="Coordinates for Blur Area (x1, y1, x2, y2):").grid(row=7, column=0, padx=10, pady=10, sticky="w")
    x1_var = tk.IntVar(value=100)
    y1_var = tk.IntVar(value=350)
    x2_var = tk.IntVar(value=600)
    y2_var = tk.IntVar(value=600)

    # Create a frame for better organization of the coordinate spinboxes
    coordinates_frame = tk.Frame(window)
    coordinates_frame.grid(row=7, column=1, columnspan=4, padx=10, pady=10)

    # X1 coordinate
    Label(coordinates_frame, text="x1:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    x1_entry = Spinbox(coordinates_frame, from_=0, to=width, textvariable=x1_var, width=5)
    x1_entry.grid(row=0, column=1, padx=5, pady=5)

    # Y1 coordinate
    Label(coordinates_frame, text="y1:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    y1_entry = Spinbox(coordinates_frame, from_=0, to=height, textvariable=y1_var, width=5)
    y1_entry.grid(row=0, column=3, padx=5, pady=5)

    # X2 coordinate
    Label(coordinates_frame, text="x2:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    x2_entry = Spinbox(coordinates_frame, from_=0, to=width, textvariable=x2_var, width=5)
    x2_entry.grid(row=1, column=1, padx=5, pady=5)

    # Y2 coordinate
    Label(coordinates_frame, text="y2:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    y2_entry = Spinbox(coordinates_frame, from_=0, to=height, textvariable=y2_var, width=5)
    y2_entry.grid(row=1, column=3, padx=5, pady=5)




    # Process video button
    Button(window, text="Process Video", command=process_video_with_gui).grid(row=8, column=1, padx=10, pady=10)

    window.mainloop()

# Start the GUI
start_gui()
