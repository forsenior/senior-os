from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton, QComboBox

from shelp.src.ui.styles.GlobalStyleSheets import get_default_label_style, get_default_input_box_style, \
    get_default_dropdown_style, get_default_settings_button_style


class MailSettingsView(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout()
        grid_layout.setColumnMinimumWidth(0, 261)

        # Labels
        label_senior_mail = QLabel("Senior email")
        label_senior_password = QLabel("Senior password")
        label_caregiver_email = QLabel("Caregiver email")
        label_email_contacts = QLabel("Email contacts (up to six)")
        label_email_pictures = QLabel("Email pictures (up to six)")
        label_send_phishing_warning = QLabel("Send phishing warning")
        label_show_url = QLabel("Show URL links in email")

        # DropDowns and Inputs
        senior_mail = QLineEdit("Enter seniors account")
        senior_password = QLineEdit("Password for seniors email account")
        caregiver_email = QLineEdit("Email account of the care giver")
        email_contacts = QLineEdit("Email contacts of the senior (please use coma to separate contacts)")
        email_pictures = QPushButton("Add pictures for selected person")

        send_phishing_warning = QComboBox()
        send_phishing_warning.addItems(["Enable", "Disable"])
        show_url = QComboBox()
        show_url.addItems(["Enable", "Disable"])

        # Add widgets to the grid
        grid_layout.addWidget(label_senior_mail, 0, 0)
        grid_layout.addWidget(senior_mail, 0, 1)

        grid_layout.addWidget(label_senior_password, 1, 0)
        grid_layout.addWidget(senior_password, 1, 1)

        grid_layout.addWidget(label_caregiver_email, 2, 0)
        grid_layout.addWidget(caregiver_email, 2, 1)

        grid_layout.addWidget(label_email_contacts, 3, 0)
        grid_layout.addWidget(email_contacts, 3, 1)

        grid_layout.addWidget(label_email_pictures, 4, 0)
        grid_layout.addWidget(email_pictures, 4, 1)

        grid_layout.addWidget(label_send_phishing_warning, 5, 0)
        grid_layout.addWidget(send_phishing_warning, 5, 1)

        grid_layout.addWidget(label_show_url, 6, 0)
        grid_layout.addWidget(show_url, 6, 1)

        self.setLayout(grid_layout)

        self.setStyleSheet(f"""
                    {get_default_label_style()}
                    {get_default_input_box_style()}
                    {get_default_dropdown_style()}
                    {get_default_settings_button_style()}
                    """)
