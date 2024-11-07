import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget,
    QHBoxLayout, QStackedWidget, QFrame, QGridLayout, QLineEdit, QComboBox, QCheckBox
)
from PyQt5.QtCore import Qt, QSize  # Include QSize here
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QStackedWidget
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy
import mediapipe as mp
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Access Control Application")
        self.setGeometry(200, 100, 1200, 800)  # Increased window size
        self.setStyleSheet("background-color: #3B4252;")  # Background color
        self.setWindowIcon(QIcon("assets/faceid.png"))

        # Initialize the main interface
        self.initUI()

        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
        self.mp_drawing = mp.solutions.drawing_utils

        # Initialize video capture for face recognition and gesture authentication
        self.video_capture = cv2.VideoCapture(0)

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
        background_pixmap = QPixmap("assets/ai_gen.webp")  # Replace with your image path
        background_label.setPixmap(background_pixmap.scaled(1000, 500, Qt.KeepAspectRatio))
        background_label.setAlignment(Qt.AlignCenter)
        home_layout.addWidget(background_label)

        # Welcome screen
        welcome_label = QLabel("Welcome to the Access Control System")
        welcome_label.setFont(QFont("Arial", 22))
        welcome_label.setStyleSheet("color: #D8DEE9;")
        welcome_label.setAlignment(Qt.AlignCenter)
        home_layout.addWidget(welcome_label)

        # Adding buttons
        button_font = QFont("Arial", 16)

        # Create horizontal layout for Face Recognition and Gesture Authentication
        special_button_layout = QHBoxLayout()

        self.face_recognition_button = QPushButton("Face Recognition")
        self.face_recognition_button.setFont(button_font)
        self.face_recognition_button.setStyleSheet(self.get_button_style())
        self.face_recognition_button.setIcon(QIcon("assets/faceid.png"))
        self.face_recognition_button.setIconSize(QSize(64, 64))
        special_button_layout.addWidget(self.face_recognition_button)

        self.gesture_auth_button = QPushButton("Gesture Authentication")
        self.gesture_auth_button.setFont(button_font)
        self.gesture_auth_button.setStyleSheet(self.get_button_style())
        self.gesture_auth_button.setIcon(QIcon("assets/img.png"))
        self.gesture_auth_button.setIconSize(QSize(64, 64))
        special_button_layout.addWidget(self.gesture_auth_button)

        # Add the special button layout to the main layout
        home_layout.addLayout(special_button_layout)

        # Create a separate grid layout for the other buttons
        button_container = QGridLayout()
        button_container.setContentsMargins(50, 20, 50, 20)

        self.access_files_button = QPushButton("Access Files/Folders")
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

        # Add view to stacked widget
        self.stacked_widget.addWidget(home_widget)

        # Button connections
        self.face_recognition_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.access_files_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.settings_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.gesture_auth_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))

    def create_face_recognition_view(self):
        # Face recognition section

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

        # Timer to update video frames for face recognition
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

    def closeEvent(self, event):
        # Stop video capture when closing the application
        self.video_capture.release()
        event.accept()
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

        # Button to open the folder dialog
        open_folder_button = QPushButton("Open Folder")
        open_folder_button.setFont(QFont("Arial", 16))
        open_folder_button.setStyleSheet(self.get_button_style())
        layout.addWidget(open_folder_button, alignment=Qt.AlignCenter)

        # Connect the button to open the folder dialog
        open_folder_button.clicked.connect(self.open_folder_dialog)

        # Back button
        back_button = QPushButton("Back to Home")
        back_button.setFont(QFont("Arial", 18))
        back_button.setStyleSheet(self.get_button_style())
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.stacked_widget.addWidget(access_files_widget)
    def open_folder_dialog(self):
        # Open folder dialog to select a folder
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt);;Images (*.png *.jpg *.jpeg)")
        if file_path:
            print(f"Selected file: {file_path}")

    def create_settings_view(self):
        settings_widget = QWidget()
        layout = QVBoxLayout()
        settings_widget.setLayout(layout)

        # Title
        label = QLabel("Settings")
        label.setFont(QFont("Arial", 24))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignCenter)

        settings_info = QLabel("Adjust your preferences below.")
        settings_info.setStyleSheet("color: white;")
        layout.addWidget(settings_info, alignment=Qt.AlignCenter)

        # Theme selection
        theme_label = QLabel("Choose Theme:")
        theme_label.setStyleSheet("color: white;")
        theme_label.setFont(QFont("Arial", 16))
        layout.addWidget(theme_label)

        theme_combobox = QComboBox()
        theme_combobox.addItems(["Light", "Dark"])
        theme_combobox.setStyleSheet("background-color: #4C566A; color: white; padding: 5px;")
        theme_combobox.setFont(QFont("Arial", 14))
        layout.addWidget(theme_combobox)

        # Notification settings
        notification_checkbox = QCheckBox("Enable Notifications")
        notification_checkbox.setStyleSheet("color: white;")
        notification_checkbox.setFont(QFont("Arial", 16))
        layout.addWidget(notification_checkbox)

        # Language selection
        language_label = QLabel("Select Language:")
        language_label.setStyleSheet("color: white;")
        language_label.setFont(QFont("Arial", 16))
        layout.addWidget(language_label)

        language_combobox = QComboBox()
        language_combobox.addItems(["English", "Spanish", "French", "German", "Chinese"])
        language_combobox.setStyleSheet("background-color: #4C566A; color: white; padding: 5px;")
        language_combobox.setFont(QFont("Arial", 14))
        layout.addWidget(language_combobox)

        # Reset settings button
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

        # Back button
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

        # Timer to update video frames for gesture recognition
        self.gesture_timer = QTimer()
        self.gesture_timer.timeout.connect(self.update_gesture_frame)
        self.gesture_timer.start(20)  # Update every 20 milliseconds

        # Back button
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

        frame = cv2.flip(frame, 1)  # Flip the frame horizontally
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        finger_count = 0
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                # List of landmark points for each finger's tip
                tips = [4, 8, 12, 16, 20]  # Thumb tip, Index finger tip, etc.
                finger_states = [False] * 5  # States for each finger (True if raised)

                # Check thumb separately due to its unique orientation
                thumb_tip = hand_landmarks.landmark[tips[0]]
                thumb_ip = hand_landmarks.landmark[2]  # Joint 2 as reference
                wrist = hand_landmarks.landmark[0]

                # Check if thumb is to the left or right of the wrist (depends on hand orientation)
                if thumb_tip.x < wrist.x:  # Right hand
                    if thumb_tip.x < thumb_ip.x:
                        finger_states[0] = True  # Thumb raised
                else:  # Left hand
                    if thumb_tip.x > thumb_ip.x:
                        finger_states[0] = True  # Thumb raised

                # Check other fingers based on tip and dip (fingers raised if tip above dip)
                for i in range(1, 5):
                    finger_tip = hand_landmarks.landmark[tips[i]]
                    finger_dip = hand_landmarks.landmark[tips[i] - 2]
                    if finger_tip.y < finger_dip.y:  # Finger is raised
                        finger_states[i] = True

                # Count raised fingers
                finger_count = sum(finger_states)

                # Display finger count on the frame
                cv2.putText(frame, f'We see: {finger_count} finger(s)', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (255, 0, 255), 2)

        # Convert frame to QImage and set it to QLabel
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