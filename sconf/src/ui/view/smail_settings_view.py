import os

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton, QComboBox, QTextEdit, QFileDialog

from configuration.models.smail_configuration import SmailConfiguration
from ui.components.ui_transformation.transformation import UiElementTransformation
from ui.convertors.value_convertors import StringValueConvertors
from ui.convertors.value_validators import Validators
from ui.styles.global_style_sheets import get_default_label_style, get_default_input_box_style, \
    get_default_dropdown_style, get_default_settings_button_style, get_default_settings_text_edit_style, \
    get_error_label_style
from ui.view_models.smail_settings_view_model import SmailViewModel


# TODO: Once initial presentation is done change this to correct binding with the view model
class MailSettingsView(QWidget):
    _smailViewModel: SmailViewModel
    _smailConfiguration: SmailConfiguration
    _configurationFolder: str

    def __init__(self, smail_configuration: SmailConfiguration, configurationFolder: str):
        super().__init__()

        self._smailConfiguration = smail_configuration
        self._smailViewModel = SmailViewModel(smail_configuration)
        self._configurationFolder = configurationFolder

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
        self.label_error = QLabel()
        self.label_error.setVisible(False)

        # DropDowns and Inputs
        senior_mail = QLineEdit(f"{self._smailConfiguration.seniorEmail if self._smailConfiguration.seniorEmail
                                                                           != "" else "Enter seniors email"}")
        senior_mail.setObjectName("seniorEmail")

        senior_password = QLineEdit(
            f"{self._smailConfiguration.seniorPassword if self._smailConfiguration.seniorPassword
                                                          != "" else "Enter password for seniors email"}")
        senior_password.setObjectName("seniorPassword")

        caregiver_email = QLineEdit(
            f"{self._smailConfiguration.careGiverEmail if self._smailConfiguration.careGiverEmail
                                                          != "" else "Enter password for seniors email"}")
        caregiver_email.setObjectName("careGiverEmail")

        self.email_contacts = QLineEdit(f"Click to edit the list of email contacts (use coma to separate)")
        self.email_contacts.mousePressEvent = self.__email_contacts_clicked_handler

        self.email_contacts_text_edit = QTextEdit(f"{StringValueConvertors.list_to_plain_text(
            self._smailConfiguration.emailContacts)}")
        self.email_contacts_text_edit.setObjectName("emailContacts")
        self.email_contacts_text_edit.setVisible(False)
        self.email_contacts_text_edit.focusOutEvent = self.__email_contacts_focus_out_handler

        email_pictures = QPushButton("Add pictures for selected person")
        email_pictures.setObjectName("emailPicturesPath")

        send_phishing_warning = QComboBox()
        send_phishing_warning.addItems(["Enable", "Disable"])
        send_phishing_warning.setObjectName("sendPhishingWarning")
        send_phishing_warning.setCurrentText(
            f"{StringValueConvertors.bool_to_string(self._smailConfiguration.sendPhishingWarning)}")

        show_url = QComboBox()
        show_url.addItems(["Enable", "Disable"])
        show_url.setObjectName("showUrlInEmail")
        show_url.setCurrentText(
            f"{StringValueConvertors.bool_to_string(self._smailConfiguration.showUrlInEmail)}")

        # Add widgets to the grid
        grid_layout.addWidget(label_senior_mail, 0, 0)
        grid_layout.addWidget(senior_mail, 0, 1)

        grid_layout.addWidget(label_senior_password, 1, 0)
        grid_layout.addWidget(senior_password, 1, 1)

        grid_layout.addWidget(label_caregiver_email, 2, 0)
        grid_layout.addWidget(caregiver_email, 2, 1)

        grid_layout.addWidget(label_email_contacts, 3, 0)
        grid_layout.addWidget(self.email_contacts, 3, 1)
        grid_layout.addWidget(self.email_contacts_text_edit, 3, 1)

        grid_layout.addWidget(label_email_pictures, 4, 0)
        grid_layout.addWidget(email_pictures, 4, 1)

        grid_layout.addWidget(label_send_phishing_warning, 5, 0)
        grid_layout.addWidget(send_phishing_warning, 5, 1)

        grid_layout.addWidget(label_show_url, 6, 0)
        grid_layout.addWidget(show_url, 6, 1)

        grid_layout.addWidget(self.label_error, 6, 1)

        senior_mail.textChanged.connect(self.__on_input_change)
        senior_password.textChanged.connect(self.__on_input_change)
        caregiver_email.textChanged.connect(self.__on_input_change)
        email_pictures.clicked.connect(self.__select_email_pictures_clicked_handler)
        send_phishing_warning.currentIndexChanged.connect(self.__on_input_change)
        show_url.currentIndexChanged.connect(self.__on_input_change)

        self.setLayout(grid_layout)

        self.setStyleSheet(f"""
                    {get_default_label_style()}
                    {get_default_input_box_style()}
                    {get_default_dropdown_style()}
                    {get_default_settings_button_style()}
                    {get_default_settings_text_edit_style()}
                    """)

    @pyqtSlot()
    def __on_input_change(self):
        sender = self.sender()
        if isinstance(sender, QLineEdit):
            self._smailViewModel.update_model(sender.objectName(),
                                              sender.text())
        if isinstance(sender, QComboBox):
            self._smailViewModel.update_model(sender.objectName(),
                                              StringValueConvertors.string_to_bool(sender.currentText()))

        if isinstance(sender, QFileDialog):
            self._smailViewModel.update_model(sender.objectName(),
                                              sender.selectedFiles())

    @pyqtSlot()
    def __select_email_pictures_clicked_handler(self):
        selected_files = UiElementTransformation.open_file_dialog(os.path.join(self._configurationFolder, "images"))
        self._smailViewModel.update_model("emailPicturesPath",
                                          selected_files)

    def __email_contacts_clicked_handler(self, event):
        UiElementTransformation.expand_widget(line_edit=self.email_contacts, text_edit=self.email_contacts_text_edit)

    def __email_contacts_focus_out_handler(self, event):
        UiElementTransformation.collapse_widget(line_edit=self.email_contacts, text_edit=self.email_contacts_text_edit)

        failing_url = ""

        for url in StringValueConvertors.plain_text_to_list(self.email_contacts_text_edit.toPlainText()):
            if Validators.validate_url(url):
                self._errorInTextInput = False
                continue
            else:
                self._errorInTextInput = True
                failing_url = url
                break

        if self._errorInTextInput:
            self.label_error.setStyleSheet(get_error_label_style())
            self.label_error.setText(f"Url is incorrect: {failing_url}")
            self.label_error.setVisible(True)
            return

        self.label_error.setVisible(False)
        self._smailViewModel.update_model(self.email_contacts_text_edit.objectName(),
                                          StringValueConvertors.plain_text_to_list(
                                              self.email_contacts_text_edit.toPlainText()))
