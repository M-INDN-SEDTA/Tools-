# AI-based subject-tracking system involving a camera and motors controlled by Arduino is quite involved and beyond the scope of a single response.
# The code uses the YOLO (You Only Look Once) object detection model to detect and track a person in the video feed. The camera is then moved based on the center coordinates of the detected person.
# Download the YOLO model files, and update the serial port information for your Arduino.

import cv2
import numpy as np
import serial
import time

# Function to send commands to Arduino via serial communication
def send_command(ser, command):
    ser.write(command.encode())

# Set up serial communication with Arduino
ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with the correct port

# Load pre-trained object detection model (e.g., YOLO or Haarcascades)
# Make sure to install OpenCV with the 'opencv-contrib-python' package for YOLO support
net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')

# Load COCO names file for YOLO
with open('coco.names', 'r') as f:
    classes = f.read().strip().split('\n')

# Initialize camera
cap = cv2.VideoCapture(0)  # Use '0' for the default camera, update if needed

while True:
    ret, frame = cap.read()

    # Object detection using YOLO
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(net.getUnconnectedOutLayersNames())

    # Get the highest confidence object (assuming one person for simplicity)
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] == 'person':
                center_x, center_y, width, height = (
                    int(detection[0] * frame.shape[1]),
                    int(detection[1] * frame.shape[0]),
                    int(detection[2] * frame.shape[1]),
                    int(detection[3] * frame.shape[0]),
                )
                x, y = int(center_x - width / 2), int(center_y - height / 2)
                boxes.append([x, y, width, height])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Move the camera based on the subject's location (simple example)
    if boxes:
        x, y, width, height = boxes[0]
        # Calculate the center of the detected subject
        center_x = x + width // 2
        center_y = y + height // 2

        # Perform camera movement control based on the center coordinates
        # Adjust the serial command format based on your Arduino code
        command = f"X{center_x}Y{center_y}\n"
        send_command(ser, command)

    # Display the result
    cv2.imshow('Object Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

