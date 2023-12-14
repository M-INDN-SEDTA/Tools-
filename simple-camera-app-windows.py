# pip install opencv-python

import cv2
import tkinter as tk
from tkinter import filedialog

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Camera App")

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

        self.capture_button = tk.Button(root, text="Capture", command=self.capture_image)
        self.capture_button.pack()

        self.quit_button = tk.Button(root, text="Quit", command=self.quit_app)
        self.quit_button.pack()

    def browse_location(self):
        folder_path = filedialog.askdirectory()
        self.save_location.set(folder_path)

    def capture_image(self):
        ret, frame = self.capture.read()
        if ret:
            save_location = self.save_location.get()
            if save_location:
                cv2.imwrite(f"{save_location}/captured_image.jpg", frame)
                print("Image captured and saved.")
            else:
                print("Please select a save location.")
        else:
            print("Failed to capture image.")

    def quit_app(self):
        self.capture.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
