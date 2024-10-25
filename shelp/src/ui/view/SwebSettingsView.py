from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton, QComboBox, QTextEdit

from shelp.src.configuration.models.SwebConfiguration import SwebConfiguration

from shelp.src.ui.convertors.ValueConvertors import StringValueConvertors
from shelp.src.ui.components.uiTransformation.Transformation import UiElementTransformation
from shelp.src.ui.styles.GlobalStyleSheets import (get_default_input_box_style,
                                                   get_default_label_style,
                                                   get_default_dropdown_style, get_default_settings_button_style,
                                                   get_default_settings_text_edit_style)
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

        self.urls_list_line_edit = QLineEdit(f"{self._swebConfiguration['urlsForWebsites']}")
        self.urls_list_line_edit.mousePressEvent = self.__urls_for_websites_clicked_handler

        self.urls_list_text_edit = QTextEdit(f"{self._swebConfiguration['urlsForWebsites']}")
        self.urls_list_line_edit.setObjectName("urlsForWebsites")
        self.urls_list_text_edit.setVisible(False)
        self.urls_list_text_edit.focusOutEvent = self.__urls_for_website_focus_out_handler

        # TODO: Finish implementation of this, not sure how, but
        website_pictures = QPushButton("Add icons of allowed websites")
        website_pictures.setObjectName("picturePaths")

        self.allowed_website_posting = QLineEdit(f"{self._swebConfiguration['allowedWebsites']}")
        self.allowed_website_posting.mousePressEvent = self.__allowed_websites_clicked_handler

        self.allowed_website_posting_text_edit = QTextEdit(f"{self._swebConfiguration['allowedWebsites']}")
        self.allowed_website_posting_text_edit.setObjectName("allowedWebsites")
        self.allowed_website_posting_text_edit.setVisible(False)
        self.allowed_website_posting_text_edit.focusOutEvent = self.__allowed_website_posting_focus_out_handler

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
        grid_layout.addWidget(self.urls_list_line_edit, 0, 1)
        grid_layout.addWidget(self.urls_list_text_edit, 0, 1)

        grid_layout.addWidget(label_website_pictures, 1, 0)
        grid_layout.addWidget(website_pictures, 1, 1)

        grid_layout.addWidget(label_send_phishing_warning, 2, 0)
        grid_layout.addWidget(send_phishing_warning, 2, 1)

        grid_layout.addWidget(label_send_phishing_form, 3, 0)
        grid_layout.addWidget(phishing_form, 3, 1)

        grid_layout.addWidget(label_allow_senior_web_posting, 4, 0)
        grid_layout.addWidget(senior_web_posting, 4, 1)

        grid_layout.addWidget(label_allowed_website_posting, 5, 0)
        grid_layout.addWidget(self.allowed_website_posting, 5, 1)
        grid_layout.addWidget(self.allowed_website_posting_text_edit, 5, 1)

        self.urls_list_text_edit.textChanged.connect(self.__on_input_change)
        website_pictures.clicked.connect(self.__on_input_change)
        send_phishing_warning.currentIndexChanged.connect(self.__on_input_change)
        phishing_form.currentIndexChanged.connect(self.__on_input_change)
        senior_web_posting.currentIndexChanged.connect(self.__on_input_change)
        self.allowed_website_posting.textChanged.connect(self.__on_input_change)

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
            self._swebViewModel.update_model(sender.objectName(),
                                             sender.text())
        if isinstance(sender, QComboBox):
            self._swebViewModel.update_model(sender.objectName(),
                                             StringValueConvertors.string_to_bool(sender.currentText()))

        if isinstance(sender, QTextEdit):
            self._swebViewModel.update_model(sender.objectName())

    def __urls_for_websites_clicked_handler(self, event):
        UiElementTransformation.expand_widget(line_edit=self.urls_list_line_edit, text_edit=self.urls_list_text_edit)

    def __allowed_websites_clicked_handler(self, event):
        UiElementTransformation.expand_widget(line_edit=self.allowed_website_posting, text_edit=self.allowed_website_posting_text_edit)

    def __urls_for_website_focus_out_handler(self, event):
        UiElementTransformation.collapse_widget(line_edit=self.urls_list_line_edit, text_edit=self.urls_list_text_edit)

    def __allowed_website_posting_focus_out_handler(self, event):
        UiElementTransformation.collapse_widget(line_edit=self.allowed_website_posting, text_edit=self.allowed_website_posting_text_edit)
