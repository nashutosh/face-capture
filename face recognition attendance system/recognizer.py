import cv2
import os
from datetime import datetime

# Directory to save captured photos
capture_dir = "captured_photos"
os.makedirs(capture_dir, exist_ok=True)

def capture_image(name):
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image from the webcam.")
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            face_roi = frame[y:y+h, x:x+w]
            # Get current date and time
            now = datetime.now()
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            file_name = f"{name}_{date_time}.jpg"
            file_path = os.path.join(capture_dir, file_name)
            cv2.imwrite(file_path, face_roi)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Write data to text file
            with open('user_data.txt', 'a') as f:
                f.write(f"Name: {name}\n")
                f.write(f"Date and Time: {date_time}\n")
                f.write(f"Image File: {file_name}\n\n")
        
        cv2.imshow('Captured Image', frame)
        # Wait for 1 second and break out of the loop if 'q' key is pressed
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def main():
    # Input student's name
    name = input("Enter your name: ")
    if name.strip():
        capture_image(name.strip())
    else:
        print("Invalid name entered. Please try again.")

if __name__ == "__main__":
    main()
