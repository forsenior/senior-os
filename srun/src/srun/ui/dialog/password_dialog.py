from PyQt5.QtWidgets import (QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QDesktopWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from srun.ui.helpers.password_helper import hash_password
from srun.ui.styles.srun_style_sheets import get_default_dialog_style


class PasswordPopup(QDialog):
    __confirmed_password_hash: str

    def __init__(self, password, initial_start_up, parent=None):
        super().__init__(parent)
        self.password_from_config = password
        initial_start_up = initial_start_up
        is_password_set = False if password == "" else True

        self.is_password_setup = True if is_password_set == False and initial_start_up == True else False

        self.setWindowTitle("Password Setup" if self.is_password_setup else "Enter Password")
        self.setFixedSize(400, 200)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.center()
        # Use consistent style with the main application
        self.setStyleSheet(get_default_dialog_style())

        # Create the layout
        layout = QVBoxLayout()

        # Message and input fields
        message = QLabel("Create a new password" if self.is_password_setup else "Enter your password")
        message.setFont(QFont('Inter', 14))

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")

        # Confirm field if in create mode

        # Buttons
        submit_button = QPushButton("Create" if self.is_password_setup else "Submit")
        submit_button.clicked.connect(self.handle_submit)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        # Add to layout
        layout.addWidget(message)
        layout.addWidget(self.password_input)
        if self.is_password_setup:
            self.confirm_password_input = QLineEdit()
            self.confirm_password_input.setEchoMode(QLineEdit.Password)
            self.confirm_password_input.setPlaceholderText("Confirm Password")
            layout.addWidget(self.confirm_password_input)
        layout.addWidget(submit_button)
        layout.addWidget(cancel_button)
        self.setLayout(layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def handle_submit(self):
        password_hash = hash_password(self.password_input.text())
        if self.is_password_setup:
            confirm_password_hash = hash_password(self.confirm_password_input.text())

        # Initial password setup:
        if ((self.password_input.text() != "")
                and self.is_password_setup
                and password_hash.hexdigest() == confirm_password_hash.hexdigest()):
            self.__confirmed_password_hash = password_hash.hexdigest()
            self.accept()
        # Regular application login
        elif ((self.password_input.text() != "")
                and not self.is_password_setup
                and password_hash.hexdigest() == self.password_from_config):
            self.accept()
        else:
            self.reject()

    def get_confirmed_password(self):
        return self.__confirmed_password_hash
