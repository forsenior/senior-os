from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QGridLayout


class MailSettingsView(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout()

        # Labels
        label_senior_mail = QLabel("Senior email")
        label_senior_password = QLabel("Senior password")
        label_caregiver_email = QLabel("Caregiver email")
        label_email_contacts = QLabel("Email contacts (up to six)")
        label_email_pictures = QLabel("Email pictures (up to six)")
        label_send_phishing_warning = QLabel("Send phishing warning")
        label_show_url = QLabel("Show URL links in email")
        label_show_url = QLabel("Show URL links in email")

        # Example UI for Mail settings
        self.email_label = QLabel("Senior email")
        self.email_input = QLineEdit("Enter senior's email")
        grid_layout.addWidget(self.email_label)
        grid_layout.addWidget(self.email_input)

        self.password_label = QLabel("Senior password")
        self.password_input = QLineEdit("Enter senior's password")
        grid_layout.addWidget(self.password_label)
        grid_layout.addWidget(self.password_input)

        self.setLayout(grid_layout)