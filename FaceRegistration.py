import cv2
import numpy as np
import dlib
import face_recognition
import os
import pandas as pd
import pickle

# Create directory for saving data if not exists
if not os.path.exists('data/'):
    os.makedirs('data/')

# Load Face Detection Model (Dlib)
detector = dlib.get_frontal_face_detector()

# Get user details
aadhaar_number = input("Enter Aadhaar Number: ")

name = input("Enter Your Name: ")

# Open Webcam
video = cv2.VideoCapture(0)

faces_data = []
framesTotal = 20  # Number of frames to capture per person
captured_frames = 0

while True:
    ret, frame = video.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()

        # Extract the face region
        face_img = frame[y:y + h, x:x + w]
        face_img = cv2.resize(face_img, (160, 160))  # Resize for FaceNet

        # Convert face to FaceNet embeddings
        face_encoding = face_recognition.face_encodings(face_img)
        if len(face_encoding) > 0:

            faces_data.append(face_encoding[0])
            captured_frames += 1

        # Draw rectangle around face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"Capturing {captured_frames}/{framesTotal}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Show webcam feed
    cv2.imshow("Register Face", frame)

    if captured_frames >= framesTotal:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

# Convert to NumPy array
faces_data = np.array(faces_data)

# Save Aadhaar, Name, and Face Embeddings
data_path = "data/faces_data.csv"

# Check if file exists
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
else:
    df = pd.DataFrame(columns=["Aadhaar", "Name"] + [f"feat_{i}" for i in range(128)])

# Add new entry
new_entry = [aadhaar_number, name] + list(faces_data.mean(axis=0))
df.loc[len(df)] = new_entry

# Save the updated dataset
df.to_csv(data_path, index=False)

print("✅ Face Registered Successfully!")
