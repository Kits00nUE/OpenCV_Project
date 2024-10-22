import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget,
    QHBoxLayout, QStackedWidget, QFrame, QGridLayout, QLineEdit, QComboBox, QCheckBox
)
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

        # Application icon (replace with path to your icon)
        self.setWindowIcon(QIcon("assets/faceid.png"))

        # Initialize the main interface
        self.initUI()
    def initUI(self):
        # Main layout elements
        main_layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Top section with title and logo
        top_layout = QHBoxLayout()
        top_frame = QFrame()
        top_frame.setLayout(top_layout)
        top_frame.setStyleSheet("background-color: #2E3440; padding: 10px; border-radius: 10px;")



        title_label = QLabel("Access Control Application")
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        title_label.setStyleSheet("color: #8FBCBB; padding-left: 20px;")
        top_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        main_layout.addWidget(top_frame)

        # Adding a stacked widget to change window content
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Creating different views
        self.create_home_view()
        self.create_face_recognition_view()
        self.create_access_files_view()
        self.create_quiz_view()
        self.create_settings_view()
        self.create_gesture_authentication_view()

        # Creating navigation bar
        self.create_navigation_bar(main_layout)
    def create_home_view(self):
        home_widget = QWidget()
        home_layout = QVBoxLayout()
        home_widget.setLayout(home_layout)
        home_layout.setAlignment(Qt.AlignCenter)

        # Adding background image
        background_label = QLabel()
        background_pixmap = QPixmap("assets/face-recognition.png")  # Replace with your image path
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

        button_container = QGridLayout()
        button_container.setContentsMargins(50, 20, 50, 20)

        self.face_recognition_button = QPushButton("Face Recognition")
        self.face_recognition_button.setFont(button_font)
        self.face_recognition_button.setStyleSheet(self.get_button_style())
        self.face_recognition_button.setIcon(QIcon("assets/faceid.png.png"))
        button_container.addWidget(self.face_recognition_button, 0, 0)

        self.access_files_button = QPushButton("Access Files/Folders")
        self.access_files_button.setFont(button_font)
        self.access_files_button.setStyleSheet(self.get_button_style())
        self.access_files_button.setIcon(QIcon("folder_icon.png"))
        button_container.addWidget(self.access_files_button, 0, 1)

        self.quiz_button = QPushButton("Quiz")
        self.quiz_button.setFont(button_font)
        self.quiz_button.setStyleSheet(self.get_button_style())
        self.quiz_button.setIcon(QIcon("quiz_icon.png"))
        button_container.addWidget(self.quiz_button, 1, 0)

        self.settings_button = QPushButton("Settings")
        self.settings_button.setFont(button_font)
        self.settings_button.setStyleSheet(self.get_button_style())
        self.settings_button.setIcon(QIcon("assets/settings.png"))
        button_container.addWidget(self.settings_button, 1, 1)

        self.gesture_auth_button = QPushButton("Gesture Authentication")
        self.gesture_auth_button.setFont(button_font)
        self.gesture_auth_button.setStyleSheet(self.get_button_style())
        self.gesture_auth_button.setIcon(QIcon("gesture_icon.png"))
        button_container.addWidget(self.gesture_auth_button, 2, 0, 1, 2)

        home_layout.addLayout(button_container)

        # Add view to stacked widget
        self.stacked_widget.addWidget(home_widget)

        # Button connections
        self.face_recognition_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.access_files_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.quiz_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.settings_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.gesture_auth_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))
    def create_face_recognition_view(self):
        # Face recognition section
        recognition_widget = QWidget()
        layout = QVBoxLayout()
        recognition_widget.setLayout(layout)

        self.video_label = QLabel("Face Recognition (Loading...)")
        self.video_label.setFont(QFont("Arial", 20))
        self.video_label.setStyleSheet("color: white;")
        layout.addWidget(self.video_label, alignment=Qt.AlignCenter)

        # Initialize video capture
        self.video_capture = cv2.VideoCapture(0)
        if not self.video_capture.isOpened():
            print("Error: Could not open video.")
            return

        # Timer to update video frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)  # Update every 20 milliseconds

        back_button = QPushButton("Back to Home")
        back_button.setFont(QFont("Arial", 20))  # Set larger font size
        back_button.setStyleSheet(self.get_button_style())  # Apply your button style
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        # Add recognition_widget to the stacked widget
        self.stacked_widget.addWidget(recognition_widget)

        # Add recognition_widget to the stacked widget
        self.stacked_widget.addWidget(recognition_widget)
    def update_frame(self):
        # Capture frame-by-frame
        ret, frame = self.video_capture.read()

        if not ret:
            print("Error: Could not read frame.")
            return

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Load Haar Cascade classifier
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        # Detect faces in the frame
        faces = face_classifier.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

        # Draw bounding boxes around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Convert frame to QImage and set it to QLabel
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        self.video_label.setPixmap(QPixmap.fromImage(q_image))
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
        back_button.setFont(QFont("Arial", 16))
        back_button.setStyleSheet(self.get_button_style())
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.stacked_widget.addWidget(access_files_widget)
    def open_folder_dialog(self):
        # Open folder dialog to select a folder
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt);;Images (*.png *.jpg *.jpeg)")
        if file_path:
            print(f"Selected file: {file_path}")
    def create_quiz_view(self):
        quiz_widget = QWidget()
        layout = QVBoxLayout()
        quiz_widget.setLayout(layout)

        label = QLabel("Quiz Section")
        label.setFont(QFont("Arial", 24))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignCenter)

        quiz_info = QLabel("Answer the quiz questions.")
        quiz_info.setStyleSheet("color: white;")
        layout.addWidget(quiz_info, alignment=Qt.AlignCenter)

        # Back button
        back_button = QPushButton("Back to Home")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.stacked_widget.addWidget(quiz_widget)
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
        reset_button.setFont(QFont("Arial", 16))
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
        back_button.setFont(QFont("Arial", 16))
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

        gesture_info = QLabel("Authenticate using gestures.")
        gesture_info.setStyleSheet("color: white;")
        layout.addWidget(gesture_info, alignment=Qt.AlignCenter)

        # Back button
        back_button = QPushButton("Back to Home")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.stacked_widget.addWidget(gesture_widget)
    def create_navigation_bar(self, main_layout):
        nav_layout = QHBoxLayout()

        home_button = QPushButton("Home")
        home_button.setFont(QFont("Arial", 16))
        home_button.setStyleSheet(self.get_nav_button_style())
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        nav_layout.addWidget(home_button)



        files_button = QPushButton("Access Files")
        files_button.setFont(QFont("Arial", 16))
        files_button.setStyleSheet(self.get_nav_button_style())
        files_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        nav_layout.addWidget(files_button)



        settings_button = QPushButton("Settings")
        settings_button.setFont(QFont("Arial", 16))
        settings_button.setStyleSheet(self.get_nav_button_style())
        settings_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        nav_layout.addWidget(settings_button)

        gesture_button = QPushButton("Gesture Auth")
        gesture_button.setFont(QFont("Arial", 16))
        gesture_button.setStyleSheet(self.get_nav_button_style())
        gesture_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        nav_layout.addWidget(gesture_button)

        main_layout.addLayout(nav_layout)
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
    def get_nav_button_style(self):
        return """
        QPushButton {
            background-color: #4C566A;
            color: white;
            border: none;
            padding: 10px;
            margin: 5px;
        }
        QPushButton:hover {
            background-color: #5E81AC;
        }
        QPushButton:pressed {
            background-color: #3B4252;
        }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
