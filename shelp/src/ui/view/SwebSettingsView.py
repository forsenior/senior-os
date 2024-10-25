from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton, QComboBox

from shelp.src.configuration.models.SwebConfiguration import SwebConfiguration

from shelp.src.ui.convertors.ValueConvertors import StringValueConvertors
from shelp.src.ui.styles.GlobalStyleSheets import (get_default_input_box_style,
                                                   get_default_label_style,
                                                   get_default_dropdown_style, get_default_settings_button_style)
from shelp.src.ui.viewModels.SwebsettingsViewModel import SwebViewModel


# TODO: Once initial presentation is done change this to correct binding with the view model
class WebSettingsView(QWidget):
    _swebConfiguration: SwebConfiguration
    _swebViewModel: SwebViewModel

    def __init__(self, sweb_configuration: SwebConfiguration):
        super().__init__()
        grid_layout = QGridLayout()
        self._swebConfiguration = sweb_configuration
        self._swebViewModel = SwebViewModel(sweb_configuration)

        # Labels
        label_urls_list = QLabel("Allowed URLs")
        label_website_pictures = QLabel("Pictures for the websites")
        label_send_phishing_warning = QLabel("Send phishing warning")
        label_send_phishing_form = QLabel("Phishing form")
        label_allow_senior_web_posting = QLabel("Senior web posting")
        label_allowed_website_posting = QLabel("Allowed website posting")

        # TODO: Change this so that upon clicking this converts to the QTextEdit to make UX better
        urls_list = QLineEdit("Allowed URLs (please use coma to separate contacts)")
        urls_list.setObjectName("urlsForWebsites")

        # TODO: Finish implementation of this, not sure how, but
        website_pictures = QPushButton("Add icons of allowed websites")
        website_pictures.setObjectName("picturePaths")

        # TODO: Change this so that upon clicking this converts to the QTextEdit to make UX better
        allowed_website_posting = QLineEdit("Websites for senior to post on (please use coma to separate contacts)")
        allowed_website_posting.setObjectName("allowedWebsites")

        send_phishing_warning = QComboBox()
        send_phishing_warning.addItems(["Enable", "Disable"])
        send_phishing_warning.setObjectName("sendPhishingWarning")
        send_phishing_warning.setCurrentText(
            f"{StringValueConvertors.bool_to_string(self._swebConfiguration['sendPhishingWarning'])}"
        )

        phishing_form = QComboBox()
        phishing_form.addItems(["Enable", "Disable"])
        phishing_form.setObjectName("phishingFormular")
        phishing_form.setCurrentText(
            f"{StringValueConvertors.bool_to_string(self._swebConfiguration['phishingFormular'])}"
        )

        senior_web_posting = QComboBox()
        senior_web_posting.addItems(["Enable", "Disable"])
        senior_web_posting.setObjectName("seniorWebsitePosting")
        senior_web_posting.setCurrentText(
            f"{StringValueConvertors.bool_to_string(self._swebConfiguration['seniorWebsitePosting'])}"
        )

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

        urls_list.textChanged.connect(self.__on_input_change)
        website_pictures.clicked.connect(self.__on_input_change)
        send_phishing_warning.currentIndexChanged.connect(self.__on_input_change)
        phishing_form.currentIndexChanged.connect(self.__on_input_change)
        senior_web_posting.currentIndexChanged.connect(self.__on_input_change)
        allowed_website_posting.textChanged.connect(self.__on_input_change)

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
            self._swebViewModel.update_model(sender.objectName(),
                                             sender.text())
        if isinstance(sender, QComboBox):
            self._swebViewModel.update_model(sender.objectName(),
                                             StringValueConvertors.string_to_bool(sender.currentText()))
