# pip install opencv-python

import cv2
import tkinter as tk
from tkinter import filedialog
from threading import Thread
import time

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera App with Recording")

        self.capture = cv2.VideoCapture(0)

        self.canvas = tk.Canvas(root, width=self.capture.get(3), height=self.capture.get(4))
        self.canvas.pack()

        self.save_location = tk.StringVar()
        self.save_location.set("")

        self.save_location_label = tk.Label(root, text="Save Location:")
        self.save_location_label.pack()

        self.save_location_entry = tk.Entry(root, textvariable=self.save_location)
        self.save_location_entry.pack()

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_location)
        self.browse_button.pack()

        self.start_recording_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_recording_button.pack()

        self.stop_recording_button = tk.Button(root, text="Stop Recording", command=self.stop_recording)
        self.stop_recording_button.pack()
        self.stop_recording_button["state"] = "disabled"

        self.quit_button = tk.Button(root, text="Quit", command=self.quit_app)
        self.quit_button.pack()

        self.is_recording = False
        self.recording_thread = None
        self.out = None

        self.update_display()

    def browse_location(self):
        folder_path = filedialog.askdirectory()
        self.save_location.set(folder_path)

    def start_recording(self):
        save_location = self.save_location.get()
        if save_location:
            self.is_recording = True
            timestamp = time.strftime("%Y%m%d%H%M%S")
            video_filename = f"{save_location}/recorded_video_{timestamp}.avi"
            self.out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'XVID'), 20.0,
                                       (int(self.capture.get(3)), int(self.capture.get(4))))
            self.recording_thread = Thread(target=self.record_video)
            self.recording_thread.start()
            self.start_recording_button["state"] = "disabled"
            self.stop_recording_button["state"] = "normal"
        else:
            print("Please select a save location.")

    def record_video(self):
        while self.is_recording:
            ret, frame = self.capture.read()
            if ret:
                self.out.write(frame)
                self.display_frame(frame)
            else:
                print("Failed to capture frame.")
                break

    def stop_recording(self):
        self.is_recording = False
        self.recording_thread.join()
        self.out.release()
        self.start_recording_button["state"] = "normal"
        self.stop_recording_button["state"] = "disabled"

    def update_display(self):
        ret, frame = self.capture.read()
        if ret:
            self.display_frame(frame)
            self.root.after(10, self.update_display)
        else:
            print("Failed to capture frame.")

    def display_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = tk.PhotoImage(master=self.canvas, data=cv2.imencode('.ppm', frame)[1].tobytes())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.root.img = img

    def quit_app(self):
        if self.is_recording:
            self.stop_recording()
        self.capture.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
