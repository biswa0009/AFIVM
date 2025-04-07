markdown
# 🗳️ Face Recognition Voting System

This is a real-time face recognition-based voting system developed in Python. It ensures secure and tamper-proof voting by allowing each registered voter to vote only once, using facial verification. Built using `OpenCV`, `face_recognition`, and `pandas`, this project integrates computer vision with voice feedback to deliver a seamless and interactive voting experience.

---

## 📌 Overview

This system:
- Uses a webcam to detect and recognize voters’ faces.
- Compares the captured face against registered faces stored in a CSV file.
- Prevents duplicate voting by checking if a person has already voted.
- Provides real-time audio feedback confirming the vote or denying a second attempt.
- Records all voting activity in a `Votes.csv` file with time and date.

---

## 📁 Project Structure

Face-Recognition-Voting-System/
│
├── data/
│   └── faces_data.csv        # Face encodings of registered voters (Aadhaar, Name, 128 features)
├── background.png            # Background UI image used for GUI overlay
├── Votes.csv                 # Auto-generated log of all votes cast
├── main.py                   # Main script running the voting system
├── README.md                 # Project documentation
└── requirements.txt          # List of required Python packages (optional)



## 🔧 Setup Instructions

### 1. ✅ Prerequisites

- Python 3.7 or above
- Webcam (internal or external)
- Windows OS (due to voice feedback via `win32com.client`)

### 2. 📦 Install Dependencies

bash
pip install opencv-python face_recognition numpy pandas pywin32 torch


> Make sure `dlib` is properly installed as it's a dependency for `face_recognition`.



## 🚀 How to Use

### Step 1: Register Voter Faces

Ensure you have a CSV file located at `data/faces_data.csv` with the following structure:


Aadhaar, Name, feat_0, feat_1, ..., feat_127
123456789012, John Doe, 0.123, -0.456, ..., 0.321


Each row represents a voter. You can generate encodings using `face_recognition.face_encodings()` from an image.

> Need help generating this? Let me know — I can provide a face registration script.

---

### Step 2: Run the Voting System

bash
python main.py

- The system will open a webcam window.
- Stand in front of the camera and wait for face detection.
- If your face is recognized and you haven’t voted yet:
  - Press `1`, `2`, `3`, or `4` on your keyboard to cast your vote:
    - `1` – BJP
    - `2` – Congress
    - `3` – AAP
    - `4` – NOTA
- You will hear: **"Your vote has been recorded. Thank you for participating in the elections."**

### If you have already voted:
- The system will say: **"You have already voted."**
- You will not be allowed to vote again.



## 📋 Voting Record

Votes are saved in `Votes.csv` with the following format:

| Aadhaar       | Name     | Vote     | Date       | Time     |
|---------------|----------|----------|------------|----------|
| 123456789012  | John Doe | AAP      | 07-04-2025 | 14:23-45 |

---

## 🗣️ Voice Feedback

This project uses Windows' built-in `SAPI.SpVoice` to give real-time voice feedback like:

- "You have already voted."
- "Your vote has been recorded."

This keeps the interaction intuitive and accessible for all voters.

---

## ⚠️ Important Notes

- **Duplicate votes are strictly prevented.** Each Aadhaar-linked face can only vote once.
- Designed for controlled environments such as schools, universities, or mock elections.
- **Not suitable for official electoral use.**

---

## 💡 Future Improvements (Optional)

- Web-based front end (Flask or Django)
- Admin dashboard for viewing stats
- QR code voter registration
- Offline vote sync mechanism
- Better face registration UI

---

## 📝 License

This project is licensed under the **MIT License**. Feel free to use and modify it for academic, personal, or experimental purposes.

---

## 🙌 Acknowledgments

- `face_recognition` by @ageitgey
- `OpenCV` for real-time video
- `pyttsx3` / `win32com` for voice feedback

---

### 👨‍💻 Author

Created with ❤️ for secure and modern voting experiences using AI and computer vision.

---

```

Let me know if you want this as a downloadable file or want help creating the face registration script as well!
