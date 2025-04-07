import cv2
import pandas as pd
import numpy as np
import face_recognition
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch
import torch

# Check for GPU availability
if torch.cuda.is_available():
    print("GPU Name:", torch.cuda.get_device_name())
    print("Number of GPU:", torch.cuda.device_count())
else:
    print("Running on CPU")

def speak(text):
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

# --- Load Registered Face Data ---
data_path = "data/faces_data.csv"
if not os.path.exists(data_path):
    print("No registered faces found! Please register before voting.")
    exit()

df = pd.read_csv(data_path)
registered_aadhaars = df['Aadhaar'].tolist()
registered_names = df['Name'].tolist()
registered_encodings = df.iloc[:, 2:].values.astype(np.float64)

# --- Setup Background and Voting CSV ---
screen_width, screen_height = 1250, 720
imgBackground = cv2.imread("finalBG.jpg")
imgBackground = cv2.resize(imgBackground, (screen_width, screen_height))
votes_file = "Votes.csv"
COL_NAMES = ['Aadhaar', 'Name', 'Vote', 'Date', 'Time']

def check_if_voted(aadhaar):
    try:
        with open(votes_file, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0] == aadhaar:
                    return True
    except FileNotFoundError:
        print("Votes file not found. It will be created.")
    return False

# --- Initialize Webcam ---
video = cv2.VideoCapture(0)

recognized_aadhaar = None
recognized_name = "Unknown"
last_face_data = None  # Store last face detection result

print("Align your face in front of the camera to cast your vote.")

frame_count = 0
process_every = 2  # Process every 2nd frame for face recognition
downscale_factor = 0.5  # Process a smaller frame for speed

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Resize frame for display (and copy for processing)
    display_frame = cv2.resize(frame, (640, 480))
    frame_copy = display_frame.copy()

    # Place the current display frame onto the background image once per loop
    bg_display = imgBackground.copy()
    bg_display[162:162 + 480, 45:45 + 640] = display_frame

    frame_count += 1

    # Process face detection every process_every frames
    if frame_count % process_every == 0:
        # Downscale the frame for faster processing
        small_frame = cv2.resize(frame_copy, (0, 0), fx=downscale_factor, fy=downscale_factor)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Reset last result if no faces detected
        if len(face_locations) == 0:
            last_face_data = None
            recognized_name = "Unknown"
            recognized_aadhaar = None
        else:
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Scale back coordinates to original size
                top = int(top / downscale_factor)
                right = int(right / downscale_factor)
                bottom = int(bottom / downscale_factor)
                left = int(left / downscale_factor)

                distances = face_recognition.face_distance(registered_encodings, face_encoding)
                best_match_index = np.argmin(distances)
                threshold = 0.5  # Lower threshold means stricter matching

                if distances[best_match_index] < threshold:
                    recognized_name = registered_names[best_match_index]
                    recognized_aadhaar = registered_aadhaars[best_match_index]
                else:
                    recognized_name = "Unknown"
                    recognized_aadhaar = None

                # Save last face detection data for reuse in skipped frames
                last_face_data = (left, top, right, bottom, recognized_name, recognized_aadhaar)

                # Draw rectangle and label on the processing frame copy
                cv2.rectangle(frame_copy, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame_copy, recognized_name, (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                # Only process the first detected face per frame
                break
    else:
        # Reuse last detected face data if available
        if last_face_data is not None:
            left, top, right, bottom, recognized_name, recognized_aadhaar = last_face_data
            cv2.rectangle(frame_copy, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame_copy, recognized_name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Update the background image with the annotated display frame
    bg_display[162:162 + 480, 45:45 + 640] = frame_copy

    # Check if the recognized face has already voted
    if recognized_name != "Unknown" and recognized_aadhaar is not None:
        if check_if_voted(recognized_aadhaar):
            speak(f"{recognized_name}, you have already voted.")
            # Instead of sleep, continue loop to allow user to exit
            cv2.imshow("Voting System", bg_display)
            if cv2.waitKey(1500) & 0xFF == ord('q'):
                break

    cv2.imshow("Voting System", bg_display)
    key = cv2.waitKey(1)

    # If a vote key is pressed (1, 2, 3, or 4) and a valid voter is recognized
    if key in [ord('1'), ord('2'), ord('3'), ord('4')] and recognized_name != "Unknown":
        if check_if_voted(recognized_aadhaar):
            speak("You have already voted.")
            continue

        votes_dict = {ord('1'): "BJP", ord('2'): "CONGRESS", ord('3'): "TMC", ord('4'): "CPIM"}
        vote = votes_dict[key]
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")

        with open(votes_file, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            # Write header if the file is empty
            if os.path.getsize(votes_file) == 0:
                writer.writerow(COL_NAMES)
            writer.writerow([recognized_aadhaar, recognized_name, vote, date, timestamp])

        speak("Your vote has been recorded. Thank you for participating in the elections.")
        break

    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
