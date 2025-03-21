import os

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QComboBox, QFileDialog, QDialog

from sconf.configuration.models.sweb_configuration import SwebConfiguration
from sconf.ui.components.ui_transformation.transformation import UiElementTransformation
from sconf.ui.convertors.value_convertors import StringValueConvertors
from sconf.ui.styles.global_style_sheets import (get_default_input_box_style,
                                                 get_default_label_style,
                                                 get_default_dropdown_style, get_default_settings_button_style,
                                                 get_default_settings_text_edit_style)
from sconf.ui.view.dialog.table_input_dialog import TablePopup
from sconf.ui.view_models.sweb_settings_view_model import SwebViewModel


# TODO: Once initial presentation is done change this to correct binding with the view model
class WebSettingsView(QWidget):
    _swebConfiguration: SwebConfiguration
    _swebViewModel: SwebViewModel

    _configurationFolder: str
    _errorInTextInput: bool

    def __init__(self, sweb_configuration: SwebConfiguration, configurationFolder: str, highlight_color: str):
        super().__init__()
        grid_layout = QGridLayout()
        self._swebConfiguration = sweb_configuration
        self._swebViewModel = SwebViewModel(sweb_configuration)
        self._configurationFolder = configurationFolder
        self.highlight_color = highlight_color

        # Labels
        label_urls_list = QLabel("Allowed URLs")

        label_allowed_website_posting = QLabel("Sites Approved for Senior Actions")
        label_allowed_website_posting.setWordWrap(True)

        self.label_error = QLabel()
        self.label_error.setVisible(False)

        self.urls_list_line_edit = QLineEdit(f"Click to edit the list of base websites")
        self.urls_list_line_edit.mousePressEvent = self.show_table


        # Add widgets to the grid
        grid_layout.addWidget(label_urls_list, 0, 0)
        grid_layout.addWidget(self.urls_list_line_edit, 0, 1)

        grid_layout.addWidget(self.label_error, 3, 1)

        self.setLayout(grid_layout)

        self.setStyleSheet(f"""
                            {get_default_label_style()}
                            {get_default_input_box_style()}
                            {get_default_dropdown_style()}
                            {get_default_settings_button_style(self.highlight_color)}
                            {get_default_settings_text_edit_style()}
                            """)

    def show_table(self, event):
        table_input = TablePopup(self._swebConfiguration.swebAllowedUrlListV2, type="web", highlight_color=self.highlight_color)

        if table_input.exec_() == QDialog.Accepted:
            print(table_input.get_updated_entries())
            self._swebViewModel.update_model("swebAllowedUrlListV2", table_input.get_updated_entries())
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
