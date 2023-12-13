# http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
#-------------------------------- 1. Python Code: --------------------------------------
# pip install opencv-python dlib pyserial    { Downlaod this library}

import cv2
import dlib
import numpy as np
import time
import serial

# Initialize Arduino connection
ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with the correct port

# Load pre-trained face detector and shape predictor
face_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Load pre-trained drowsiness detection model (simplified for demo)
# For a more accurate model, consider training on a larger dataset
# Model should output 1 for drowsiness and 0 for awake
# For simplicity, using a dummy model here
def predict_drowsiness(landmarks):
    # Dummy model
    return np.random.choice([0, 1])

# Open camera
cap = cv2.VideoCapture(0)  # Use '0' for the default camera, update if needed

# Variables for state tracking
state = "Awake"
start_time = None
recording = False
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = None

# Main loop
while True:
    ret, frame = cap.read()

    # Detect faces
    faces = face_detector(frame)
    for face in faces:
        landmarks = landmark_predictor(frame, face)

        # Dummy function for drowsiness detection
        drowsiness_prediction = predict_drowsiness(landmarks)

        if drowsiness_prediction == 1:
            if state != "Drowsy":
                state = "Drowsy"
                start_time = time.time()
                recording = True
                out = cv2.VideoWriter('drowsiness_video.avi', fourcc, 20.0, (640, 480))

        elif state == "Drowsy" and time.time() - start_time > 5:
            state = "Awake"
            recording = False
            if out:
                out.release()

        if recording:
            out.write(frame)

        # Display state on the frame
        cv2.putText(frame, f"State: {state}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display frame
    cv2.imshow('Drowsiness Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()


#-------------------------------- 2. Arduino Code: --------------------------------------

char state;

void setup() {
  Serial.begin(9600);  // Set the baud rate to match the Python script
}

void loop() {
  if (Serial.available() > 0) {
    state = Serial.read();

    if (state == 'D') {
      // Perform action for drowsiness (e.g., beep sound)
      tone(8, 1000, 1000);  // Pin 8, 1000 Hz, 1000 ms
    } else if (state == 'F') {
      // Perform action for fatigue (e.g., display a message)
      Serial.println("You are in fatigue");
    }
  }
}


#-------------------------------- 1. Python Code ( with video record ) : --------------------------------------                       

import cv2
import dlib
import numpy as np
import time
import serial

# Initialize Arduino connection
ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with the correct port

# Load pre-trained face detector and shape predictor
face_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Load pre-trained drowsiness detection model (simplified for demo)
# For a more accurate model, consider training on a larger dataset
# Model should output 1 for drowsiness and 0 for awake
# For simplicity, using a dummy model here
def predict_drowsiness(landmarks):
    # Dummy model
    return np.random.choice([0, 1])

# Open camera
cap = cv2.VideoCapture(0)  # Use '0' for the default camera, update if needed

# Variables for state tracking
state = "Awake"
start_time = None
recording = False
buffer_time = 5  # Buffer time before state change to record video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = None

# Main loop
while True:
    ret, frame = cap.read()

    # Detect faces
    faces = face_detector(frame)
    for face in faces:
        landmarks = landmark_predictor(frame, face)

        # Dummy function for drowsiness detection
        drowsiness_prediction = predict_drowsiness(landmarks)

        if drowsiness_prediction == 1:
            if state != "Drowsy":
                state = "Drowsy"
                start_time = time.time() - buffer_time
                recording = True
                out = cv2.VideoWriter(f'{state.lower()}_video.avi', fourcc, 20.0, (640, 480))

        elif state != "Awake" and time.time() - start_time > buffer_time:
            state = "Awake"
            recording = False
            if out:
                out.release()

        if recording:
            out.write(frame)

        # Display state on the frame
        cv2.putText(frame, f"State: {state}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display frame
    cv2.imshow('Drowsiness Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
                       
