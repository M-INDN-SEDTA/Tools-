# pip install opencv-python pyautogui numpy

import cv2
import numpy as np
import pyautogui
import tkinter as tk
from tkinter import filedialog

# Function to start screen recording
def start_recording(output_path, frames_per_second, resolution):
    screen = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_path, fourcc, frames_per_second, resolution)

    while True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)

        cv2.imshow("Recording", frame)
        if cv2.waitKey(1) == ord("q"):
            break

    out.release()
    cv2.destroyAllWindows()

# Function to capture a specific window or area
def capture_area(output_path, x, y, width, height):
    img = pyautogui.screenshot(region=(x, y, width, height))
    img.save(output_path)

# Function to get user input for recording parameters
def get_recording_options():
    frames_per_second = int(input("Enter frames per second: "))
    width = int(input("Enter width (0 for full screen): "))
    height = int(input("Enter height (0 for full screen): "))
    resolution = (width, height)
    return frames_per_second, resolution

# Function to get user input for capture area parameters
def get_capture_options():
    x = int(input("Enter X coordinate of top-left corner: "))
    y = int(input("Enter Y coordinate of top-left corner: "))
    width = int(input("Enter width of capture area: "))
    height = int(input("Enter height of capture area: "))
    return x, y, width, height

# Function to get the output path from the user
def get_output_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi")])
    return file_path

if __name__ == "__main__":
    print("1. Record Full Screen")
    print("2. Record Specific Area")
    choice = int(input("Enter your choice (1 or 2): "))

    if choice == 1:
        output_path = get_output_path()
        frames_per_second, resolution = get_recording_options()
        start_recording(output_path, frames_per_second, resolution)
    elif choice == 2:
        output_path = get_output_path()
        x, y, width, height = get_capture_options()
        capture_area(output_path, x, y, width, height)
    else:
        print("Invalid choice.")
