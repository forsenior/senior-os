import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton, QComboBox, QTextEdit, QFileDialog, \
    QTableWidget, QHeaderView, QTableWidgetItem

from sconf.configuration.models.sweb_configuration import SwebConfiguration
from sconf.ui.components.ui_transformation.transformation import UiElementTransformation
from sconf.ui.convertors.value_convertors import StringValueConvertors
from sconf.ui.convertors.value_validators import Validators
from sconf.ui.styles.global_style_sheets import (get_default_input_box_style,
                                                 get_default_label_style,
                                                 get_default_dropdown_style, get_default_settings_button_style,
                                                 get_default_settings_text_edit_style, get_error_label_style,
                                                 get_default_table_style)
from sconf.ui.view_models.sweb_settings_view_model import SwebViewModel


# TODO: Once initial presentation is done change this to correct binding with the view model
class WebSettingsView(QWidget):
    _swebConfiguration: SwebConfiguration
    _swebViewModel: SwebViewModel

    _configurationFolder: str
    _errorInTextInput: bool

    def __init__(self, sweb_configuration: SwebConfiguration, configurationFolder: str):
        super().__init__()
        grid_layout = QGridLayout()
        self._swebConfiguration = sweb_configuration
        self._swebViewModel = SwebViewModel(sweb_configuration)
        self._configurationFolder = configurationFolder

        # Labels
        label_urls_list = QLabel("Allowed URLs")

        # TODO: Remove as it will be set by Protection Level
        # label_send_phishing_warning = QLabel("Send phishing warning")
        # label_send_phishing_form = QLabel("Phishing form")
        # label_allow_senior_web_posting = QLabel("Senior web posting")
        label_allowed_website_posting = QLabel("Sites Approved for Senior Actions")
        label_allowed_website_posting.setWordWrap(True)

        self.label_error = QLabel()
        self.label_error.setVisible(False)

        self.urls_list_line_edit = QLineEdit(f"Click to edit the list of base websites")
        self.urls_list_line_edit.mousePressEvent = self.show_table

        self.allowed_website_posting = QLineEdit("")
        self.allowed_website_posting.setPlaceholderText(f"Click to edit the list of allowed websites for senior actions"
                                                        f"(use coma to separate)")
        self.allowed_website_posting.mousePressEvent = self.__allowed_websites_clicked_handler

        self.allowed_website_posting_text_edit = QTextEdit(f"{StringValueConvertors.list_to_plain_text(
            self._swebConfiguration.allowedWebsites)}")
        self.allowed_website_posting_text_edit.setObjectName("allowedWebsites")
        self.allowed_website_posting_text_edit.setVisible(False)
        self.allowed_website_posting_text_edit.focusOutEvent = self.__allowed_website_posting_focus_out_handler

        # Table widget for URLs and icons (initially hidden)
        self.url_table = QTableWidget(6, 2)
        self.url_table.setHorizontalHeaderLabels(["URL", "Icon"])
        self.url_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.url_table.setShowGrid(False)
        self.url_table.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.url_table.resizeColumnsToContents()

        self.url_table.verticalHeader().setVisible(False)
        self.url_table.horizontalHeader().setVisible(False)

        # Fill table with data from config model
        index = 1
        for row, entry in enumerate(self._swebConfiguration.swebAllowedUrlListV2):
            url_item = QTableWidgetItem(entry[f"url{index}"])
            self.url_table.setItem(row, 0, url_item)

            icon_button = QPushButton("Select Icon")
            icon_button.setText(entry[f"icon{index}"])
            icon_button.setStyleSheet(get_default_settings_button_style())
            icon_button.clicked.connect(lambda _, r=row: self.select_icon(r))
            self.url_table.setCellWidget(row, 1, icon_button)
            index += 1

        # Buttons to save or cancel
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMaximumWidth(256)
        self.save_button.setMaximumWidth(256)

        # Hide table initially
        self.url_table.hide()
        self.cancel_button.hide()
        self.save_button.hide()

        # Add widgets to the grid
        grid_layout.addWidget(label_urls_list, 0, 0)
        grid_layout.addWidget(self.urls_list_line_edit, 0, 1)
        grid_layout.addWidget(self.url_table, 0, 1)
        grid_layout.addWidget(self.save_button, 1, 1)
        grid_layout.addWidget(self.cancel_button, 1, 2)

        grid_layout.addWidget(label_allowed_website_posting, 2, 0)
        grid_layout.addWidget(self.allowed_website_posting, 2, 1)
        grid_layout.addWidget(self.allowed_website_posting_text_edit, 2, 1)

        grid_layout.addWidget(self.label_error, 3, 1)

        self.allowed_website_posting.textChanged.connect(self.__on_input_change)
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
        self._swebViewModel.update_model("swebAllowedUrlListV2", new_entries)

        self.save_button.hide()
        self.cancel_button.hide()
        self.url_table.hide()

    def cancel_entries(self):
        # Hide table without saving changes
        self.save_button.hide()
        self.cancel_button.hide()
        self.url_table.hide()

    @pyqtSlot()
    def __on_input_change(self):
        sender = self.sender()
        if isinstance(sender, QLineEdit):
            self._swebViewModel.update_model(sender.objectName(),
                                             sender.text())

        if isinstance(sender, QComboBox):
            self._swebViewModel.update_model(sender.objectName(),
                                             StringValueConvertors.string_to_bool(sender.currentText()))

        if isinstance(sender, QFileDialog):
            self._smailViewModel.update_model(sender.objectName(),
                                              sender.selectedFiles())

    @pyqtSlot()
    def __select_website_pictures_clicked_handler(self):
        selected_files = UiElementTransformation.open_file_dialog(os.path.join(self._configurationFolder, "images"))

        self._swebViewModel.update_model("picturePaths",
                                         selected_files)

    def __allowed_websites_clicked_handler(self, event):
        UiElementTransformation.expand_widget(line_edit=self.allowed_website_posting,
                                              text_edit=self.allowed_website_posting_text_edit)

    def __allowed_website_posting_focus_out_handler(self, event):
        UiElementTransformation.collapse_widget(line_edit=self.allowed_website_posting,
                                                text_edit=self.allowed_website_posting_text_edit)

        failing_url = ""

        for url in StringValueConvertors.plain_text_to_list(self.allowed_website_posting_text_edit.toPlainText()):
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
        self._swebViewModel.update_model(self.allowed_website_posting_text_edit.objectName(),
                                         StringValueConvertors.plain_text_to_list(
                                             self.allowed_website_posting_text_edit.toPlainText()))
