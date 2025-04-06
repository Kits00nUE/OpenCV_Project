
# Access Control Application

An advanced access control system that combines facial recognition, gesture-based authentication, and file encryption to provide secure file management.

## Overview

This project implements a state-of-the-art access control system designed to protect sensitive files. The application uses biometric authentication—specifically, facial recognition and hand gesture detection—to verify users before allowing access. Upon successful authentication, the system can encrypt or decrypt files using AES encryption, ensuring that data remains secure against unauthorized access.

## Features

- **Facial Recognition:**  
  Utilizes the [face_recognition](https://github.com/ageitgey/face_recognition) library to capture and compare facial features in real-time via a webcam.

- **Gesture Authentication:**  
  Leverages [MediaPipe](https://google.github.io/mediapipe/) and [OpenCV](https://opencv.org/) to detect and count hand gestures (e.g., the number of fingers shown) as an additional layer of verification.

- **File Encryption/Decryption:**  
  Uses the AES algorithm provided by [PyCryptodome](https://www.pycryptodome.org/en/latest/) to securely encrypt and decrypt files, protecting user data from unauthorized access.

- **User-Friendly GUI:**  
  Developed with [PyQt5](https://pypi.org/project/PyQt5/), the graphical interface offers intuitive navigation and control over the authentication process and file management functions.

## Technologies Used

- **Python:** Core programming language.
- **PyQt5:** For building the graphical user interface.
- **OpenCV:** For image and video processing.
- **MediaPipe:** For real-time gesture detection.
- **face_recognition:** For facial feature extraction and identification.
- **PyCryptodome:** For implementing AES encryption/decryption.

## Usage

1. **Running the Application:**

   ```bash
   python main.py
   ```

2. **User Workflow:**

   - **Home Screen:**  
     Users can choose to unlock the system, block files, or add a new face for authentication.
     
   - **Facial Recognition:**  
     The application captures the user's face through a webcam and compares it against a stored reference encoding.
     
   - **Gesture Authentication:**  
     Upon successful facial verification, users are prompted to perform a gesture by showing a specified number of fingers.
     
   - **File Management:**  
     Once authenticated, users can block (encrypt) and unblock (decrypt) files, ensuring data security.
     
   - **Settings:**  
     Customize the application’s preferences including theme, language, and notifications.

## Authors
- [@GrzegorzDrozdz](https://github.com/GrzegorzDrozdz)
- [@Taiq-UE](https://github.com/Taiq-UE)
- [@Kits00nUE](https://github.com/Kits00nUE)

