from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QLineEdit, QGridLayout

from configuration.models.global_configuration import GlobalConfiguration
from ui.convertors.value_convertors import StringValueConvertors
from ui.styles.global_style_sheets import get_default_label_style, get_default_input_box_style, \
    get_default_dropdown_style
from ui.view_models.global_settings_view_model import GlobalViewModel


# TODO: Once initial presentation is done change this to correct binding with the view model
class GlobalSettingsView(QWidget):
    _globalViewModel: GlobalViewModel
    _globalConfiguration: GlobalConfiguration

    def __init__(self, global_configuration: GlobalConfiguration):
        super().__init__()
        # Create layout for labels and input fields
        grid_layout = QGridLayout()
        self._globalConfiguration = global_configuration
        self._globalViewModel = GlobalViewModel(global_configuration)

        # Labels
        label_language = QLabel("Language")
        label_alert_color = QLabel("Alert color (in hex)")
        label_highlight_color = QLabel("Highlight color (in hex)")
        label_protection_level = QLabel("Protection Level")

        # Dropdowns and Inputs
        combo_language = QComboBox()
        combo_language.addItems(["English", "German", "Czech"])
        combo_language.setObjectName("language")
        combo_language.setCurrentText(StringValueConvertors.country_code_to_language(self._globalConfiguration.language))

        input_alert_color = QLineEdit(f"Select value of the alert in hex values (current is "
                                      f"{self._globalConfiguration.alertColor})")
        input_alert_color.setObjectName("alertColor")

        input_highlight_color = QLineEdit(f"Select value of the alert in hex values (current is "
                                          f"{self._globalConfiguration.highlightColor})")
        input_highlight_color.setObjectName("highlightColor")

        combo_protection_level = QComboBox()
        combo_protection_level.addItems(["PL1", "PL2", "PL3"])
        combo_protection_level.setObjectName("protectionLevel")
        combo_language.setCurrentText(f"{StringValueConvertors.int_to_protection_level(
            self._globalConfiguration.protectionLevel)}")

        # Add widgets to the grid
        grid_layout.addWidget(label_language, 0, 0)
        grid_layout.addWidget(combo_language, 0, 1)

        grid_layout.addWidget(label_alert_color, 1, 0)
        grid_layout.addWidget(input_alert_color, 1, 1)

        grid_layout.addWidget(label_highlight_color, 2, 0)
        grid_layout.addWidget(input_highlight_color, 2, 1)

        grid_layout.addWidget(label_protection_level, 3, 0)
        grid_layout.addWidget(combo_protection_level, 3, 1)

        combo_language.currentIndexChanged.connect(self.__on_input_change)
        input_alert_color.textChanged.connect(self.__on_input_change)
        input_highlight_color.textChanged.connect(self.__on_input_change)
        combo_protection_level.currentIndexChanged.connect(self.__on_input_change)

        # Set widget layout
        self.setLayout(grid_layout)

        # Apply styling
        self.setStyleSheet(f"""
                            {get_default_label_style()}
                            {get_default_input_box_style()}
                            {get_default_dropdown_style()}
                        """)

    @pyqtSlot()
    def __on_input_change(self):
        sender = self.sender()

        if isinstance(sender, QLineEdit):
            self._globalViewModel.update_model(sender.objectName(),
                                               sender.text())
        if sender.objectName() == "protectionLevel" and isinstance(sender, QComboBox):
            self._globalViewModel.update_model(sender.objectName(),
                                               StringValueConvertors.protection_level_to_int(sender.currentText()))

        if sender.objectName() == "language" and isinstance(sender, QComboBox):
            print(StringValueConvertors.language_to_country_code(sender.currentText()))
            self._globalViewModel.update_model(sender.objectName(),
                                               StringValueConvertors.language_to_country_code(sender.currentText()))
