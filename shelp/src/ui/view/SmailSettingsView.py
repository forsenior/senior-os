from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton, QComboBox

from shelp.src.configuration.models.SmailConfiguration import SmailConfiguration

from shelp.src.ui.styles.GlobalStyleSheets import get_default_label_style, get_default_input_box_style, \
    get_default_dropdown_style, get_default_settings_button_style
from shelp.src.ui.viewModels.SmailSettingsViewModel import SmailViewModel
from shelp.src.ui.convertors.ValueConvertors import StringValueConvertors


# TODO: Once initial presentation is done change this to correct binding with the view model
class MailSettingsView(QWidget):
    _smailViewModel: SmailViewModel
    _smailConfiguration: SmailConfiguration

    def __init__(self, smail_configuration: SmailConfiguration):
        super().__init__()

        self._smailConfiguration = smail_configuration
        self._smailViewModel = SmailViewModel(smail_configuration)

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
        senior_mail = QLineEdit(f"{self._smailConfiguration['seniorEmail'] if self._smailConfiguration['seniorEmail']
                                                                              != ""
        else "Enter seniors email"}")
        senior_mail.setObjectName("seniorEmail")

        senior_password = QLineEdit(
            f"{self._smailConfiguration['seniorPassword'] if self._smailConfiguration['seniorPassword']
                                                             != ""
            else "Enter password "
                 "for seniors email"}")
        senior_password.setObjectName("seniorPassword")

        caregiver_email = QLineEdit(
            f"{self._smailConfiguration['careGiverEmail'] if self._smailConfiguration['careGiverEmail']
                                                             != ""
            else "Enter password "
                 "for seniors email"}")
        caregiver_email.setObjectName("careGiverEmail")

        # TODO: Change this so that upon clicking this converts to the QTextEdit to make UX better
        email_contacts = QLineEdit("Email contacts of the senior (please use coma to separate contacts)")
        email_contacts.setObjectName("emailContacts")

        # TODO: Finish implementation of this, not sure how, but
        email_pictures = QPushButton("Add pictures for selected person")
        email_pictures.setObjectName("emailPicturesPath")

        send_phishing_warning = QComboBox()
        send_phishing_warning.addItems(["Enable", "Disable"])
        send_phishing_warning.setObjectName("sendPhishingWarning")
        send_phishing_warning.setCurrentText(
            f"{StringValueConvertors.string_to_bool(self._smailConfiguration['sendPhishingWarning'])}")

        show_url = QComboBox()
        show_url.addItems(["Enable", "Disable"])
        show_url.setObjectName("showUrlInEmail")
        show_url.setCurrentText(
            f"{StringValueConvertors.bool_to_string(self._smailConfiguration['showUrlInEmail'])}")

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

        senior_mail.textChanged.connect(self.__on_input_change)
        senior_password.textChanged.connect(self.__on_input_change)
        caregiver_email.textChanged.connect(self.__on_input_change)
        email_contacts.textChanged.connect(self.__on_input_change)
        email_pictures.clicked.connect(self.__on_input_change)
        send_phishing_warning.currentIndexChanged.connect(self.__on_input_change)
        show_url.currentIndexChanged.connect(self.__on_input_change)

        self.setLayout(grid_layout)

        self.setStyleSheet(f"""
                    {get_default_label_style()}
                    {get_default_input_box_style()}
                    {get_default_dropdown_style()}
                    {get_default_settings_button_style()}
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
