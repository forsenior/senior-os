from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton, QComboBox

from shelp.src.ui.styles.GlobalStyleSheets import (get_default_input_box_style,
                                                   get_default_label_style,
                                                   get_default_dropdown_style, get_default_settings_button_style)


class WebSettingsView(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout()

        self.setStyleSheet(f"""
                    {get_default_label_style()}
                    {get_default_input_box_style()}
                    {get_default_input_box_style()}
                """)

        # Labels
        label_urls_list = QLabel("Allowed URLs")
        label_website_pictures = QLabel("Pictures for the websites")
        label_send_phishing_warning = QLabel("Send phishing warning")
        label_send_phishing_form = QLabel("Phishing form")
        label_allow_senior_web_posting = QLabel("Senior web posting")
        label_allowed_website_posting = QLabel("Allowed website posting")

        urls_list = QLineEdit("Allowed URLs (please use coma to separate contacts)")
        website_pictures = QPushButton("Add icons of allowed websites")
        allowed_website_posting = QPushButton("Websites for senior to post on (please use coma to separate contacts)")

        send_phishing_warning = QComboBox()
        send_phishing_warning.addItems(["Enable", "Disable"])
        phishing_form = QComboBox()
        phishing_form.addItems(["Enable", "Disable"])
        senior_web_posting = QComboBox()
        senior_web_posting.addItems(["Enable", "Disable"])

        # Add widgets to the grid
        grid_layout.addWidget(label_urls_list, 0, 0)
        grid_layout.addWidget(urls_list, 0, 1)

        grid_layout.addWidget(label_website_pictures, 1, 0)
        grid_layout.addWidget(website_pictures, 1, 1)

        grid_layout.addWidget(label_send_phishing_warning, 2, 0)
        grid_layout.addWidget(send_phishing_warning, 2, 1)

        grid_layout.addWidget(label_send_phishing_form, 3, 0)
        grid_layout.addWidget(phishing_form, 3, 1)

        grid_layout.addWidget(label_allow_senior_web_posting, 4, 0)
        grid_layout.addWidget(senior_web_posting, 4, 1)

        grid_layout.addWidget(label_allowed_website_posting, 5, 0)
        grid_layout.addWidget(allowed_website_posting, 5, 1)

        self.setLayout(grid_layout)

        self.setStyleSheet(f"""
                            {get_default_label_style()}
                            {get_default_input_box_style()}
                            {get_default_dropdown_style()}
                            {get_default_settings_button_style()}
                            """)
