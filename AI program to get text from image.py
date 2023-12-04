import cv2
from PIL import Image
import pytesseract

def ocr_from_frame(frame):
    # Convert OpenCV BGR format to RGB
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Convert the image array to a PIL image
    pil_image = Image.fromarray(rgb_image)
    
    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(pil_image)

    return text

if __name__ == "__main__":
    # Open the camera (you may need to change the camera index)
    cap = cv2.VideoCapture(0)

    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        # Perform OCR on the captured frame
        result_text = ocr_from_frame(frame)

        # Display the original frame and OCR result
        cv2.imshow("Original Frame", frame)
        print("OCR Result:")
        print(result_text)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()
