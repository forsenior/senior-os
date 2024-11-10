import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QGridLayout, QPushButton, QComboBox, QFileDialog
, QTableWidget, QHeaderView, QTableWidgetItem, QHBoxLayout)

from sconf.configuration.models.smail_configuration import SmailConfiguration
from sconf.ui.components.ui_transformation.transformation import UiElementTransformation
from sconf.ui.convertors.value_convertors import StringValueConvertors
from sconf.ui.convertors.value_validators import Validators
from sconf.ui.styles.global_style_sheets import get_default_label_style, get_default_input_box_style, \
    get_default_dropdown_style, get_default_settings_button_style, get_default_settings_text_edit_style, \
    get_error_label_style, get_default_table_style
from sconf.ui.view_models.smail_settings_view_model import SmailViewModel


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
        self.label_email_contacts = QLabel("Email contacts (up to six)")

        # TODO: Remove as it will be set by Protection Level
        # label_send_phishing_warning = QLabel("Send phishing warning")
        # label_show_url = QLabel("Show URL links in email")

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

        self.email_contacts = QLineEdit(f"Click to edit the list of email contacts")
        self.email_contacts.setReadOnly(True)
        self.email_contacts.mousePressEvent = self.show_table

        # Table widget for URLs and icons (initially hidden)
        self.url_table = QTableWidget(6, 2)
        self.url_table.setHorizontalHeaderLabels(["Email", "Icon"])
        self.url_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.url_table.setShowGrid(False)
        self.url_table.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.url_table.resizeColumnsToContents()

        self.url_table.verticalHeader().setVisible(False)
        self.url_table.horizontalHeader().setVisible(False)

        # Fill table with data from config model
        index = 1
        for row, entry in enumerate(self._smailConfiguration.emailContactsV2):
            url_item = QTableWidgetItem(entry[f"email{index}"])
            self.url_table.setItem(row, 0, url_item)

            icon_button = QPushButton("Select Icon")
            icon_button.setText(entry[f"icon{index}"])
            icon_button.setStyleSheet(get_default_settings_button_style())
            icon_button.clicked.connect(lambda _, r=row: self.select_icon(r))
            self.url_table.setCellWidget(row, 1, icon_button)
            index += 1

        # Buttons to save or cancel
        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMaximumWidth(256)
        self.save_button.setMaximumWidth(256)

        # Hide table initially
        self.url_table.hide()
        self.cancel_button.hide()
        self.save_button.hide()

        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)

        grid_layout.addWidget(label_senior_mail, 0, 0)
        grid_layout.addWidget(senior_mail, 0, 1)

        grid_layout.addWidget(label_senior_password, 1, 0)
        grid_layout.addWidget(senior_password, 1, 1)

        grid_layout.addWidget(label_caregiver_email, 2, 0)
        grid_layout.addWidget(caregiver_email, 2, 1)

        grid_layout.addWidget(self.label_email_contacts, 3, 0)
        grid_layout.addWidget(self.email_contacts, 3, 1)
        grid_layout.addWidget(self.url_table, 3, 1, 1, 2)
        grid_layout.addWidget(self.save_button, 4, 1)
        grid_layout.addWidget(self.cancel_button, 4, 2)

        grid_layout.addWidget(self.label_error, 4, 1)

        senior_mail.textChanged.connect(self.__on_input_change)
        senior_password.textChanged.connect(self.__on_input_change)
        caregiver_email.textChanged.connect(self.__on_input_change)
        self.save_button.clicked.connect(self.save_entries)
        self.cancel_button.clicked.connect(self.cancel_entries)

        self.setLayout(grid_layout)

        self.setStyleSheet(f"""
                    {get_default_label_style()}
                    {get_default_input_box_style()}
                    {get_default_dropdown_style()}
                    {get_default_settings_button_style()}
                    {get_default_settings_text_edit_style()}
                    {get_default_table_style()}
                    """)

    def show_table(self, event):
        # Show the table when the line edit is clicked
        self.email_contacts.hide()
        self.save_button.show()
        self.cancel_button.show()
        self.url_table.show()

    def select_icon(self, row):
        # Open file dialog to select icon and update button label to path
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Icon")
        if file_path:
            icon_button = self.url_table.cellWidget(row, 1)
            icon_button.setText(file_path)  # Show path on button for preview

    def save_entries(self, event):
        # Save changes to model
        index = 1
        new_entries = []
        for row in range(6):
            url = self.url_table.item(row, 0).text() if self.url_table.item(row, 0) else ""
            icon_path = self.url_table.cellWidget(row, 1).text() if self.url_table.cellWidget(row, 1) else ""
            if url:  # Only save if URL is not empty
                new_entries.append({f"email{index}": url, f"icon{index}": icon_path})
            index += 1
        self._smailViewModel.update_model("emailContactsV2", new_entries)

        self.email_contacts.show()
        self.save_button.hide()
        self.cancel_button.hide()
        self.url_table.hide()

    def cancel_entries(self):
        # Hide table without saving changes
        self.email_contacts.show()
        self.save_button.hide()
        self.cancel_button.hide()
        self.url_table.hide()

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
