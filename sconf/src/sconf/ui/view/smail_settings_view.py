import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QGridLayout, QComboBox, QFileDialog, QDialog)

from sconf.configuration.models.global_configuration import GlobalConfiguration
from sconf.configuration.models.smail_configuration import SmailConfiguration
from sconf.ui.components.ui_transformation.transformation import UiElementTransformation
from sconf.ui.convertors.value_convertors import StringValueConvertors
from sconf.ui.convertors.value_validators import Validators
from sconf.ui.styles.global_style_sheets import get_default_label_style, get_default_input_box_style, \
    get_default_dropdown_style, get_default_settings_button_style, get_default_settings_text_edit_style, \
    get_error_label_style, get_default_table_style
from sconf.ui.view_models.smail_settings_view_model import SmailViewModel
from sconf.ui.view.dialog.table_input_dialog import TablePopup


# TODO: Once initial presentation is done change this to correct binding with the view model
class MailSettingsView(QWidget):
    _smailViewModel: SmailViewModel
    _smailConfiguration: SmailConfiguration
    _globalConfiguration: GlobalConfiguration
    _configurationFolder: str

    def __init__(self, smail_configuration: SmailConfiguration,
                 globalConfiguration: GlobalConfiguration,
                 configurationFolder: str,
                 highlight_color: str):
        super().__init__()

        self._smailConfiguration = smail_configuration
        self._globalConfiguration = globalConfiguration
        self._smailViewModel = SmailViewModel(smail_configuration, globalConfiguration)
        self._configurationFolder = configurationFolder
        self.highlight_color = highlight_color

        grid_layout = QGridLayout()
        grid_layout.setColumnMinimumWidth(0, 261)
        grid_layout.setRowStretch(4, 0)

        # Labels
        label_senior_mail = QLabel("Senior email")
        label_senior_password = QLabel("Senior password")
        label_caregiver_email = QLabel("Caregiver email")
        self.label_email_contacts = QLabel("Email contacts (up to six)")

        self.label_error = QLabel()
        self.label_error.setVisible(False)

        # DropDowns and Inputs
        self.senior_mail = QLineEdit(f"{self._smailConfiguration.seniorEmail if self._smailConfiguration.seniorEmail
                                                                           != "" else "Enter seniors email"}")
        self.senior_mail.setObjectName("seniorEmail")

        self.senior_password = QLineEdit(
            f"{self._smailConfiguration.seniorPassword if self._smailConfiguration.seniorPassword
                                                          != "" else "Enter password for seniors email"}")
        self.senior_password.setObjectName("seniorPassword")
        self.senior_password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.caregiver_email = QLineEdit(
            f"{self._globalConfiguration.careGiverEmail if self._globalConfiguration.careGiverEmail
                                                          != "" else "Enter email for the caregiver"}")
        self.caregiver_email.setObjectName("careGiverEmail")

        self.email_contacts = QLineEdit(f"Click to edit the list of email contacts")
        self.email_contacts.setReadOnly(True)
        self.email_contacts.mousePressEvent = self.show_table

        grid_layout.addWidget(label_senior_mail, 0, 0)
        grid_layout.addWidget(self.senior_mail, 0, 1)

        grid_layout.addWidget(label_senior_password, 1, 0)
        grid_layout.addWidget(self.senior_password, 1, 1)

        grid_layout.addWidget(label_caregiver_email, 2, 0)
        grid_layout.addWidget(self.caregiver_email, 2, 1)

        grid_layout.addWidget(self.label_email_contacts, 3, 0)
        grid_layout.addWidget(self.email_contacts, 3, 1)

        grid_layout.addWidget(self.label_error, 4, 1)

        self.senior_mail.textChanged.connect(self.__on_input_change)
        self.senior_password.textChanged.connect(self.__on_input_change)
        self.caregiver_email.textChanged.connect(self.__on_input_change)

        self.setLayout(grid_layout)

        self.setStyleSheet(f"""
                    {get_default_label_style()}
                    {get_default_input_box_style()}
                    {get_default_dropdown_style()}
                    {get_default_settings_button_style(self.highlight_color)}
                    {get_default_settings_text_edit_style()}
                    {get_default_table_style()}
                    """)

    def show_table(self, event):
        table_input = TablePopup(self._smailConfiguration.emailContactsV2, highlight_color=self.highlight_color)

        if table_input.exec_() == QDialog.Accepted:
            print(table_input.get_updated_entries())
            self._smailViewModel.update_model("emailContactsV2", table_input.get_updated_entries())

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
