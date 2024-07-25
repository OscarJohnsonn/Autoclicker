from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFrame, QHBoxLayout, QGridLayout, QComboBox
from PyQt5.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor

import sys
import pyautogui
import random
import json

class AutoClickerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.click_mouse)
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.click_count = 0
        self.is_dragging = False
        self.start_drag_pos = QPoint()
        self.click_position = None
        self.countdown = 0
        self.load_settings()

    def init_ui(self):
        self.setWindowTitle("Simple AutoClicker")
        self.setGeometry(100, 100, 320, 380)
        self.setStyleSheet("background-color: #353535; color: white;")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.outer_layout = QVBoxLayout()
        self.outer_layout.setContentsMargins(10, 10, 10, 10)
        self.outer_layout.setSpacing(10)

        self.inner_frame = QFrame()
        self.inner_frame.setStyleSheet("background-color: #35363B; border-radius: 10px;")

        self.inner_layout = QVBoxLayout()
        self.inner_layout.setContentsMargins(10, 10, 10, 10)
        self.inner_layout.setSpacing(10)

        self.title_bar = QWidget()
        self.title_bar.setStyleSheet("background-color: #35363B;")
        self.title_bar_layout = QHBoxLayout()
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.title_bar_layout.setSpacing(5)

        self.title_label = QLabel("Simple AutoClicker")
        self.title_label.setStyleSheet("color: white;")
        self.title_label.setFont(QFont("Arial", 14))
        self.title_bar_layout.addWidget(self.title_label)
        self.title_bar_layout.addStretch()

        self.min_button = QPushButton()
        self.min_button.setText("🟡")
        self.min_button.setFixedSize(30, 30)
        self.min_button.setStyleSheet("""
            QPushButton {
                background-color: #35363B;
                border: none;
                color: yellow;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #3C3C3C;
            }
            QPushButton:focus {
                outline: none;
            }
        """)
        self.min_button.clicked.connect(self.showMinimized)
        self.title_bar_layout.addWidget(self.min_button)

        self.close_button = QPushButton()
        self.close_button.setText("❌")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #35363B;
                border: none;
                color: red;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #3C3C3C;
            }
            QPushButton:focus {
                outline: none;
            }
        """)
        self.close_button.clicked.connect(self.close)
        self.title_bar_layout.addWidget(self.close_button)

        self.title_bar.setLayout(self.title_bar_layout)
        self.title_bar.mousePressEvent = self.title_bar_mouse_press_event
        self.title_bar.mouseMoveEvent = self.title_bar_mouse_move_event
        self.inner_layout.addWidget(self.title_bar)

        self.freq_label = QLabel("Click Frequency (seconds):")
        self.freq_label.setAlignment(Qt.AlignCenter)
        self.freq_label.setFont(QFont("Arial", 12))
        self.inner_layout.addWidget(self.freq_label)

        self.freq_entry = QLineEdit("0.1")
        self.freq_entry.setAlignment(Qt.AlignCenter)
        self.freq_entry.setFont(QFont("Arial", 12))
        self.freq_entry.setFixedHeight(30)
        self.freq_entry.setStyleSheet("background-color: white; color: black; border-radius: 5px;")
        self.inner_layout.addWidget(self.freq_entry)

        self.click_type_label = QLabel("Click Type:")
        self.click_type_label.setAlignment(Qt.AlignCenter)
        self.click_type_label.setFont(QFont("Arial", 12))
        self.inner_layout.addWidget(self.click_type_label)

        # Custom style for the combo box with the drop-down indicator inside the label
        self.click_type_combo = QComboBox()
        self.click_type_combo.addItems(["Left Click", "Right Click", "Double Click"])
        self.click_type_combo.setFixedHeight(30)
        self.click_type_combo.setFont(QFont("Arial", 12))
        self.click_type_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: black;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
                background: transparent;
                width: 15px;
            }
            QComboBox::down-arrow {
                image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAHCAYAAAAheVY0AAAApElEQVR42mJYwAAjUAEWgAEmAEe3A4IeALY0ADP4Da4aA5Q3H1Fgq4Cz4QAJhgAzvR4O5kAAAAASUVORK5CYII=); /* Small down arrow image */
                subcontrol-position: right;
                subcontrol-origin: padding;
            }
            QComboBox::drop-down:hover {
                background-color: #3C3C3C;
            }
        """)
        self.inner_layout.addWidget(self.click_type_combo)

        self.position_button = QPushButton("Set Click Position")
        self.position_button.setFixedSize(200, 30)
        self.position_button.setFont(QFont("Arial", 12))
        self.position_button.setStyleSheet("""
            QPushButton {
                background-color: #5C64EE;
                border-radius: 5px;
                color: white;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #4A54D1;
            }
            QPushButton:focus {
                outline: none;
            }
        """)
        self.position_button.clicked.connect(self.start_countdown)
        self.inner_layout.addWidget(self.position_button, alignment=Qt.AlignCenter)

        self.start_button = QPushButton("Start")
        self.start_button.setFixedSize(120, 60)
        self.start_button.setFont(QFont("Arial", 14))
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #5C64EE;
                border-radius: 15px;
                color: white;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #4A54D1;
            }
            QPushButton:focus {
                outline: none;
            }
        """)
        self.start_button.clicked.connect(self.start_clicking)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setFixedSize(120, 60)
        self.stop_button.setFont(QFont("Arial", 14))
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #5C64EE;
                border-radius: 15px;
                color: white;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #4A54D1;
            }
            QPushButton:focus {
                outline: none;
            }
        """)
        self.stop_button.clicked.connect(self.stop_clicking)
        self.stop_button.setEnabled(False)

        self.button_layout = QGridLayout()
        self.button_layout.addWidget(self.start_button, 0, 0)
        self.button_layout.addWidget(self.stop_button, 0, 1)
        self.button_layout.setHorizontalSpacing(20)
        self.button_layout.setVerticalSpacing(0)
        self.inner_layout.addLayout(self.button_layout)

        self.click_counter_label = QLabel("Clicks: 0")
        self.click_counter_label.setAlignment(Qt.AlignCenter)
        self.click_counter_label.setFont(QFont("Arial", 12))
        self.inner_layout.addWidget(self.click_counter_label)

        self.reset_button = QPushButton("Reset Counter")
        self.reset_button.setFixedSize(200, 30)
        self.reset_button.setFont(QFont("Arial", 12))
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #5C64EE;
                border-radius: 5px;
                color: white;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #4A54D1;
            }
            QPushButton:focus {
                outline: none;
            }
        """)
        self.reset_button.clicked.connect(self.reset_counter)
        self.inner_layout.addWidget(self.reset_button, alignment=Qt.AlignCenter)

        self.save_button = QPushButton("Save Settings")
        self.save_button.setFixedSize(200, 30)
        self.save_button.setFont(QFont("Arial", 12))
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #5C64EE;
                border-radius: 5px;
                color: white;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #4A54D1;
            }
            QPushButton:focus {
                outline: none;
            }
        """)
        self.save_button.clicked.connect(self.save_settings)
        self.inner_layout.addWidget(self.save_button, alignment=Qt.AlignCenter)

        self.inner_frame.setLayout(self.inner_layout)
        self.outer_layout.addWidget(self.inner_frame)
        self.setLayout(self.outer_layout)

        # Add an animation for the window's appearance
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(500)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.start()

    def start_countdown(self):
        self.countdown = 2
        self.position_button.setText(f"Position in {self.countdown} seconds")
        self.countdown_timer.start(1000)  # Update countdown every second

    def update_countdown(self):
        self.countdown -= 1
        if self.countdown <= 0:
            self.countdown_timer.stop()
            self.record_position()
        else:
            self.position_button.setText(f"Position in {self.countdown} seconds")

    def record_position(self):
        self.click_position = pyautogui.position()
        self.position_button.setText(f"Position: {self.click_position}")

    def start_clicking(self):
        try:
            interval = float(self.freq_entry.text())
            if '-' in self.freq_entry.text():
                min_interval, max_interval = map(float, self.freq_entry.text().split('-'))
                interval = random.uniform(min_interval, max_interval)
            self.timer.start(int(interval * 1000))
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        except ValueError:
            self.freq_entry.setText("Invalid input")

    def stop_clicking(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def click_mouse(self):
        click_type = self.click_type_combo.currentText()
        if self.click_position:
            x, y = self.click_position
        else:
            x, y = pyautogui.position()

        if click_type == "Left Click":
            pyautogui.click(x, y)
        elif click_type == "Right Click":
            pyautogui.rightClick(x, y)
        elif click_type == "Double Click":
            pyautogui.doubleClick(x, y)

        self.click_count += 1
        self.click_counter_label.setText(f"Clicks: {self.click_count}")

    def reset_counter(self):
        self.click_count = 0
        self.click_counter_label.setText("Clicks: 0")

    def save_settings(self):
        settings = {
            "frequency": self.freq_entry.text(),
            "click_type": self.click_type_combo.currentText(),
            "click_position": self.click_position
        }
        with open("settings.json", "w") as file:
            json.dump(settings, file)

    def load_settings(self):
        try:
            with open("settings.json", "r") as file:
                settings = json.load(file)
                self.freq_entry.setText(settings.get("frequency", "0.1"))
                self.click_type_combo.setCurrentText(settings.get("click_type", "Left Click"))
                self.click_position = tuple(settings.get("click_position", (None, None)))
                if self.click_position[0] is not None and self.click_position[1] is not None:
                    self.position_button.setText(f"Position: {self.click_position}")
        except FileNotFoundError:
            pass

    def title_bar_mouse_press_event(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.start_drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def title_bar_mouse_move_event(self, event):
        if self.is_dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.start_drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.is_dragging = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoClickerApp()
    window.show()
    sys.exit(app.exec_())
