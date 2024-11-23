import sys
import mediapipe as mp
import face_recognition
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget,
    QHBoxLayout, QStackedWidget, QFrame, QGridLayout, QLineEdit, QComboBox, QCheckBox
)
from PyQt5.QtCore import Qt, QSize  # Include QSize here
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QStackedWidget

from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage
import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QInputDialog, QMessageBox
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import os
import time
import random
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Access Control Application")
        self.setGeometry(200, 100, 1200, 800)
        self.setStyleSheet("background-color: #3B4252;")
        self.setWindowIcon(QIcon("assets/faceid.png"))

        self.initUI()

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
        self.mp_drawing = mp.solutions.drawing_utils

        self.video_capture = cv2.VideoCapture(0)

        # Sprawdź, czy plik z twarzą użytkownika już istnieje
        self.face_folder = "face"
        self.face_file = os.path.join(self.face_folder, "user_face.npy")
        if os.path.exists(self.face_file):
            self.reference_encoding = np.load(self.face_file)
            print("Reference face encoding loaded.")
            self.status = "blocked"
        else:
            self.status = "unblocked"
            self.reference_encoding = None

    def initUI(self):
        main_layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        top_layout = QHBoxLayout()
        top_frame = QFrame()
        top_frame.setLayout(top_layout)
        top_frame.setStyleSheet("background-color: #2E3440; padding: 10px; border-radius: 10px;")

        title_label = QLabel("Access Control Application")
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        title_label.setStyleSheet("color: #8FBCBB; padding-left: 20px;")
        top_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        main_layout.addWidget(top_frame)

        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        self.create_home_view()
        self.create_face_recognition_view()
        self.create_access_files_view()
        self.create_settings_view()
        self.create_gesture_authentication_view()

    def create_home_view(self):
        home_widget = QWidget()
        home_layout = QVBoxLayout()
        home_widget.setLayout(home_layout)
        home_layout.setAlignment(Qt.AlignCenter)

        # Adding background image
        background_label = QLabel()
        background_pixmap = QPixmap("assets/ai_gen.webp")
        background_label.setPixmap(background_pixmap.scaled(1000, 500, Qt.KeepAspectRatio))
        background_label.setAlignment(Qt.AlignCenter)
        home_layout.addWidget(background_label)

        welcome_label = QLabel("Welcome to the Access Control System")
        welcome_label.setFont(QFont("Arial", 22))
        welcome_label.setStyleSheet("color: #D8DEE9;")
        welcome_label.setAlignment(Qt.AlignCenter)
        home_layout.addWidget(welcome_label)

        button_font = QFont("Arial", 16)

        special_button_layout = QHBoxLayout()

        self.unlock_button = QPushButton("Unlock")
        self.unlock_button.setFont(button_font)
        self.unlock_button.setStyleSheet(self.get_button_style())
        self.unlock_button.setIcon(QIcon("assets/faceid.png"))
        self.unlock_button.setIconSize(QSize(64, 64))
        special_button_layout.addWidget(self.unlock_button)

        self.block_button = QPushButton("Block")
        self.block_button.setFont(button_font)
        self.block_button.setStyleSheet(self.get_button_style())
        self.block_button.setIcon(QIcon("assets/img.png"))
        self.block_button.setIconSize(QSize(64, 64))
        special_button_layout.addWidget(self.block_button)

        self.add_face_button = QPushButton("Add Face")
        self.add_face_button.setFont(button_font)
        self.add_face_button.setStyleSheet(self.get_button_style())
        self.add_face_button.setIcon(QIcon("assets/faceid.png"))
        self.add_face_button.setIconSize(QSize(64, 64))
        special_button_layout.addWidget(self.add_face_button)

        home_layout.addLayout(special_button_layout)

        button_container = QGridLayout()
        button_container.setContentsMargins(50, 20, 50, 20)

        self.access_files_button = QPushButton("Access Files")
        self.access_files_button.setFont(button_font)
        self.access_files_button.setStyleSheet(self.get_button_style())
        self.access_files_button.setIcon(QIcon("assets/img_1.png"))
        self.access_files_button.setIconSize(QSize(50, 50))
        button_container.addWidget(self.access_files_button, 0, 0)

        self.settings_button = QPushButton("Settings")
        self.settings_button.setFont(button_font)
        self.settings_button.setStyleSheet(self.get_button_style())
        self.settings_button.setIcon(QIcon("assets/img_2.png"))
        self.settings_button.setIconSize(QSize(50, 50))
        button_container.addWidget(self.settings_button, 1, 0)

        home_layout.addLayout(button_container)

        self.stacked_widget.addWidget(home_widget)

        self.unlock_button.clicked.connect(self.start_unlock_process)
        self.block_button.clicked.connect(self.block_function)
        self.add_face_button.clicked.connect(self.add_face)
        self.access_files_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.settings_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))

    def start_unlock_process(self):
        print("Starting face recognition process")
        self.stacked_widget.setCurrentIndex(1)
        self.face_timer = QTimer()
        self.face_timer.timeout.connect(self.check_face_recognition)
        self.face_timer.start(20)  # Check every 20 milliseconds
        self.face_recognition_start_time = time.time()

    def check_face_recognition(self):
        if self.reference_encoding is None:
            print("No reference face encoding available.")
            self.show_error_message("Error", "No reference face encoding available.")
            return

        ret, frame = self.video_capture.read()
        if not ret:
            print("Error: Could not read frame.")
            return

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces([self.reference_encoding], face_encoding, tolerance=0.5)
            if True in matches:
                print("Face recognized")
                if time.time() - self.face_recognition_start_time >= 3:
                    print("Face recognized for 3 seconds")
                    self.face_timer.stop()
                    self.stacked_widget.setCurrentIndex(4)
                    self.start_finger_counting()
                    return
            else:
                self.face_recognition_start_time = time.time()

        # Aktualizacja obrazu na ekranie
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        self.video_label.setPixmap(QPixmap.fromImage(q_image))
        self.video_label.update()  # Ensure QLabel is updated

    def start_finger_counting(self):
        self.finger_count_timer = QTimer()
        self.finger_count_timer.timeout.connect(self.check_finger_count)
        self.finger_count_timer.start(20)  # Check every 20 milliseconds
        self.finger_count_start_time = time.time()
        self.target_finger_count = random.randint(1, 5)
        self.show_finger_count_message()
        self.finger_recognition_start_time = None

    def show_finger_count_message(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Show Fingers")
        msg_box.setText(f"Please show {self.target_finger_count} fingers.")
        msg_box.setIcon(QMessageBox.Information)
        QTimer.singleShot(1500, msg_box.accept)
        msg_box.exec_()

    def check_finger_count(self):
        if time.time() - self.finger_count_start_time > 10:
            self.finger_count_timer.stop()
            self.show_error_message("Error", "Time is up! Failed to show the correct number of fingers.")
            self.stacked_widget.setCurrentIndex(0)
            return False

        ret, frame = self.video_capture.read()
        if not ret:
            print("Error: Could not read frame.")
            return

        results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                finger_count = self.count_fingers(hand_landmarks)
                print(f"Detected {finger_count} fingers")
                if finger_count == self.target_finger_count:
                    if self.finger_recognition_start_time is None:
                        self.finger_recognition_start_time = time.time()
                    elif time.time() - self.finger_recognition_start_time >= 3:
                        self.finger_count_timer.stop()
                        print("Unlocked")
                        self.stacked_widget.setCurrentIndex(0)
                        self.folders_unlocked()
                        return True
                else:
                    self.finger_recognition_start_time = None

    def count_fingers(self, hand_landmarks):
        finger_tips = [4, 8, 12, 16, 20]
        finger_count = 0

        for tip in finger_tips:
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                finger_count += 1

        return finger_count

    def create_face_recognition_view(self):
        recognition_widget = QWidget()
        layout = QVBoxLayout()
        recognition_widget.setLayout(layout)

        label = QLabel("Face Recognition")
        label.setFont(QFont("Arial", 24))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignCenter)

        self.video_label = QLabel("Face Recognition (Loading...)")
        self.video_label.setFont(QFont("Arial", 20))
        self.video_label.setStyleSheet("color: white;")
        layout.addWidget(self.video_label, alignment=Qt.AlignCenter)

        self.face_timer = QTimer()
        self.face_timer.timeout.connect(self.update_face_frame)
        self.face_timer.start(20)  # Update every 20 milliseconds
        back_button = QPushButton("Back to Home")
        back_button.setFont(QFont("Arial", 18))
        back_button.setStyleSheet(self.get_button_style())
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.stacked_widget.addWidget(recognition_widget)

    def update_face_frame(self):
        ret, frame = self.video_capture.read()
        if not ret:
            print("Error: Could not read frame.")
            return

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_classifier.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        self.video_label.setPixmap(QPixmap.fromImage(q_image))
        self.video_label.update()  # Ensure QLabel is updated

    def create_gesture_authentication_view(self):
        gesture_widget = QWidget()
        layout = QVBoxLayout()
        gesture_widget.setLayout(layout)

        label = QLabel("Gesture Authentication")
        label.setFont(QFont("Arial", 24))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignCenter)

        self.gesture_video_label = QLabel("Gesture Authentication (Loading...)")
        self.gesture_video_label.setFont(QFont("Arial", 20))
        self.gesture_video_label.setStyleSheet("color: white;")
        layout.addWidget(self.gesture_video_label, alignment=Qt.AlignCenter)

        self.gesture_timer = QTimer()
        self.gesture_timer.timeout.connect(self.update_gesture_frame)
        self.gesture_timer.start(20)

        back_button = QPushButton("Back to Home")
        back_button.setFont(QFont("Arial", 18))
        back_button.setStyleSheet(self.get_button_style())
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.stacked_widget.addWidget(gesture_widget)

    def update_gesture_frame(self):
        ret, frame = self.video_capture.read()
        if not ret:
            print("Error: Could not read frame.")
            return

        results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        self.gesture_video_label.setPixmap(QPixmap.fromImage(q_image))
        self.gesture_video_label.update()  # Ensure QLabel is updated

    def block_function(self):
        # Placeholder for block functionality
        pass

    def closeEvent(self, event):
        self.video_capture.release()
        event.accept()

    def get_button_style1(self):
        return """
        QPushButton {
            background-color: #2196F3; /* Blue background */
            color: white; /* White text */
            border-radius: 15px; /* Rounded corners */
            padding: 10px 20px; /* Top and bottom padding */
            font-size: 16px; /* Text size */
            font-weight: bold; /* Bold text */
            border: 2px solid #2196F3; /* Border same as background */
            transition: all 0.3s ease; /* Smooth transition */
            min-width: 200px; /* Set a minimum width for all buttons */
            min-height: 50px; /* Set a minimum height for all buttons */
            max-width: 200px; /* Ensure buttons do not exceed a certain width */
            max-height: 50px; /* Ensure buttons do not exceed a certain height */
        }
        QPushButton:hover {
            background-color: #1976D2; /* Slightly darker blue on hover */
            border: 2px solid #1976D2; /* Border changes with hover */
        }
        QPushButton:pressed {
            background-color: #1565C0; /* Even darker blue when pressed */
            border: 2px solid #1565C0; /* Border changes on press */
        }
        """

    def show_unlocked_message(self):
        self.status = "unblocked"
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Unlocked")
        msg_box.setText("Folders Unlocked")
        msg_box.setIcon(QMessageBox.Information)
        QTimer.singleShot(15000, msg_box.accept)
        msg_box.exec_()

    def add_face(self):
        if self.status != "unblocked":
            self.show_error_message("Error", "You must unlock the system before adding a new face.")
            return

        ret, frame = self.video_capture.read()
        if not ret:
            self.show_error_message("Error", "Could not read frame.")
            return

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        if len(face_locations) == 0:
            self.show_error_message("Error", "No face detected.")
            return

        face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
        self.reference_encoding = face_encoding

        # Save the face encoding to a file
        if not os.path.exists(self.face_folder):
            os.makedirs(self.face_folder)
        np.save(self.face_file, self.reference_encoding)

        self.status = "unblocked"
        self.show_confirmation_message("Success", "Face added successfully.")

    def folders_unlocked(self):
        self.show_unlocked_message()

    def show_error_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.exec_()

    def show_confirmation_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()    

    def create_access_files_view(self):

        access_files_widget = QWidget()
        layout = QVBoxLayout()
        access_files_widget.setLayout(layout)

        label = QLabel("Access Your Files")
        label.setFont(QFont("Arial", 24))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignCenter)

        file_info = QLabel("This section allows you to open your files.")
        file_info.setStyleSheet("color: white;")
        layout.addWidget(file_info, alignment=Qt.AlignCenter)

        open_file_button = QPushButton("Select File")
        open_file_button.setFont(QFont("Arial", 16))
        open_file_button.setStyleSheet(self.get_button_style1())
        layout.addWidget(open_file_button, alignment=Qt.AlignCenter)

        open_file_button.clicked.connect(self.open_file_dialog)

        self.selected_file_label = QLabel("No file selected")
        self.selected_file_label.setStyleSheet("color: white; font-size: 16px;")
        layout.addWidget(self.selected_file_label, alignment=Qt.AlignCenter)

        open_button = QPushButton("Open")
        open_button.setFont(QFont("Arial", 16))
        open_button.setStyleSheet(self.get_button_style1())
        layout.addWidget(open_button, alignment=Qt.AlignCenter)

        open_button.clicked.connect(self.open_selected_file)

        block_file_button = QPushButton("Block File")
        block_file_button.setFont(QFont("Arial", 16))
        block_file_button.setStyleSheet(self.get_button_style1())
        layout.addWidget(block_file_button, alignment=Qt.AlignCenter)

        block_file_button.clicked.connect(self.block_file_function)

        add_user_button = QPushButton("Add User")
        add_user_button.setFont(QFont("Arial", 16))
        add_user_button.setStyleSheet(self.get_button_style1())
        layout.addWidget(add_user_button, alignment=Qt.AlignCenter)

        add_user_button.clicked.connect(self.add_user_function)

        back_button = QPushButton("Back to Home")
        back_button.setFont(QFont("Arial", 18))
        back_button.setStyleSheet(self.get_button_style1())
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.stacked_widget.addWidget(access_files_widget)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "",
                                                   "All Files (*);;Text Files (*.txt);;Images (*.png *.jpg *.jpeg);;PDF Files (*.pdf)")

        if file_path:
            self.selected_file_label.setText(f"Selected File: {file_path}")
    def open_selected_file(self):
        file_path = self.selected_file_label.text().replace("Selected File: ", "")

        if file_path == "No file selected":
            self.show_error_message("Error", "No file has been selected.")
            return


        print(f"Opening file: {file_path}")
        self.show_confirmation_message(f"The file '{file_path}' is now opened.")

    def block_file_function(self):
        confirmation = QMessageBox.question(self, "Block File", "Are you sure you want to block this file?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            print("File blocked successfully.")
            self.show_confirmation_message("The selected file has been blocked.")

    def add_user_function(self):
        username, ok = QInputDialog.getText(self, "Add User", "Enter username:")
        if ok and username:
            print(f"User '{username}' added successfully.")
            self.show_confirmation_message(f"User '{username}' added successfully.")

    def show_confirmation_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()

    def show_error_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.exec_()

    def get_button_style(self):
        return "background-color: #4CAF50; color: white; border-radius: 5px; padding: 10px; font-size: 16px;"

    def create_settings_view(self):
        settings_widget = QWidget()
        layout = QVBoxLayout()
        settings_widget.setLayout(layout)

        label = QLabel("Settings")
        label.setFont(QFont("Arial", 24))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignCenter)

        settings_info = QLabel("Adjust your preferences below.")
        settings_info.setStyleSheet("color: white;")
        layout.addWidget(settings_info, alignment=Qt.AlignCenter)

        theme_label = QLabel("Choose Theme:")
        theme_label.setStyleSheet("color: white;")
        theme_label.setFont(QFont("Arial", 16))
        layout.addWidget(theme_label)

        theme_combobox = QComboBox()
        theme_combobox.addItems(["Light", "Dark"])
        theme_combobox.setStyleSheet("background-color: #4C566A; color: white; padding: 5px;")
        theme_combobox.setFont(QFont("Arial", 14))
        layout.addWidget(theme_combobox)

        notification_checkbox = QCheckBox("Enable Notifications")
        notification_checkbox.setStyleSheet("color: white;")
        notification_checkbox.setFont(QFont("Arial", 16))
        layout.addWidget(notification_checkbox)

        language_label = QLabel("Select Language:")
        language_label.setStyleSheet("color: white;")
        language_label.setFont(QFont("Arial", 16))
        layout.addWidget(language_label)

        language_combobox = QComboBox()
        language_combobox.addItems(["English", "Spanish", "French", "German", "Chinese"])
        language_combobox.setStyleSheet("background-color: #4C566A; color: white; padding: 5px;")
        language_combobox.setFont(QFont("Arial", 14))
        layout.addWidget(language_combobox)

        reset_button = QPushButton("Reset to Default Settings")
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #BF616A;
                color: white;
                border-radius: 8px;
                padding: 10px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #D08770;
            }
            QPushButton:pressed {
                background-color: #A3BE8C;
            }
        """)
        reset_button.setFont(QFont("Arial", 18))
        layout.addWidget(reset_button, alignment=Qt.AlignCenter)

        back_button = QPushButton("Back to Home")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #88C0D0;
                color: white;
                border-radius: 8px;
                padding: 10px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
            QPushButton:pressed {
                background-color: #5E81AC;
            }
        """)
        back_button.setFont(QFont("Arial", 18))
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.stacked_widget.addWidget(settings_widget)

    def create_gesture_authentication_view(self):
        gesture_widget = QWidget()
        layout = QVBoxLayout()
        gesture_widget.setLayout(layout)

        label = QLabel("Gesture Authentication")
        label.setFont(QFont("Arial", 24))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignCenter)

        self.gesture_video_label = QLabel("Gesture Authentication (Loading...)")
        self.gesture_video_label.setFont(QFont("Arial", 20))
        self.gesture_video_label.setStyleSheet("color: white;")
        layout.addWidget(self.gesture_video_label, alignment=Qt.AlignCenter)

        self.gesture_timer = QTimer()
        self.gesture_timer.timeout.connect(self.update_gesture_frame)
        self.gesture_timer.start(20)

        back_button = QPushButton("Back to Home")
        back_button.setFont(QFont("Arial", 18))
        back_button.setStyleSheet(self.get_button_style())
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.stacked_widget.addWidget(gesture_widget)

    def update_gesture_frame(self):
        ret, frame = self.video_capture.read()
        if not ret:
            print("Error: Could not read frame.")
            return

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        finger_count = 0
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)


                tips = [4, 8, 12, 16, 20]
                finger_states = [False] * 5

                thumb_tip = hand_landmarks.landmark[tips[0]]
                thumb_ip = hand_landmarks.landmark[2]
                wrist = hand_landmarks.landmark[0]

                if thumb_tip.x < wrist.x:
                    if thumb_tip.x < thumb_ip.x:
                        finger_states[0] = True
                else:
                    if thumb_tip.x > thumb_ip.x:
                        finger_states[0] = True


                for i in range(1, 5):
                    finger_tip = hand_landmarks.landmark[tips[i]]
                    finger_dip = hand_landmarks.landmark[tips[i] - 2]
                    if finger_tip.y < finger_dip.y:
                        finger_states[i] = True

                finger_count = sum(finger_states)
                cv2.putText(frame, f'We see: {finger_count} finger(s)', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (255, 0, 255), 2)
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        self.gesture_video_label.setPixmap(QPixmap.fromImage(q_image))

    def get_button_style(self):
        return """
        QPushButton {
            background-color: #88C0D0;
            color: white;
            border-radius: 8px;
            padding: 10px;
            margin: 5px;
        }
        QPushButton:hover {
            background-color: #81A1C1;
        }
        QPushButton:pressed {
            background-color: #5E81AC;
        }
        """
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())