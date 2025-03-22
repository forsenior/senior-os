import scryptum

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QPushButton

from vcolorpicker import getColor, hex2rgb, rgb2hex

from sconf.configuration.models.global_configuration import GlobalConfiguration
from sconf.configuration.models.smail_configuration import SmailConfiguration
from sconf.configuration.models.sos_configuration import SOSConfiguration
from sconf.configuration.models.sweb_configuration import SwebConfiguration
from sconf.ui.convertors.value_convertors import StringValueConvertors
from sconf.ui.styles.global_style_sheets import get_default_label_style, get_default_input_box_style, \
    get_default_dropdown_style, get_default_config_button_style
from sconf.ui.view_models.global_settings_view_model import GlobalViewModel


class GlobalSettingsView(QWidget):
    _globalViewModel: GlobalViewModel
    _globalConfiguration: GlobalConfiguration
    _sosConfiguration: SOSConfiguration

    def __init__(self, global_configuration: GlobalConfiguration,
                 sweb_configuration: SwebConfiguration,
                 smail_configuration: SmailConfiguration,
                 sos_configuration: SOSConfiguration
                 ):
        super().__init__()
        # Create layout for labels and input fields
        grid_layout = QGridLayout()
        self._globalConfiguration = global_configuration
        self._sosConfiguration = sos_configuration
        self._globalViewModel = GlobalViewModel(global_configuration, sweb_configuration, smail_configuration)

        # Labels
        label_language = QLabel("Language")
        label_alert_color = QLabel("Alert color (in hex)")
        label_highlight_color = QLabel("Highlight color (in hex)")
        label_protection_level = QLabel("Protection Level")
        label_current_guid = QLabel("Add current computer")

        # Dropdowns and Inputs
        combo_language = QComboBox()
        combo_language.addItems(["English", "German", "Czech"])
        combo_language.setObjectName("language")
        combo_language.setCurrentText(
            StringValueConvertors.country_code_to_language(self._globalConfiguration.language))

        input_alert_color = QLineEdit()
        input_alert_color.setPlaceholderText(f"Select value of the alert in hex values (current is #"
                                             f"{self._globalConfiguration.alertColor})")
        input_alert_color.setObjectName("alertColor")
        input_alert_color.mousePressEvent = self.__on_alert_color_clicked

        input_highlight_color = QLineEdit()
        input_highlight_color.setPlaceholderText(f"Select value of the highlight in hex values (current is #"
                                                 f"{self._globalConfiguration.highlightColor})")
        input_highlight_color.setObjectName("highlightColor")
        input_highlight_color.mousePressEvent = self.__on_highlight_color_clicked

        combo_protection_level = QComboBox()
        combo_protection_level.addItems(["PL1", "PL2", "PL3"])
        combo_protection_level.setObjectName("protectionLevel")
        combo_language.setCurrentText(f"{StringValueConvertors.int_to_protection_level(
            self._globalConfiguration.protectionLevel)}")

        button_current_computer = QPushButton()
        button_current_computer.setText(f"Add computer to allowed")
        button_current_computer.setObjectName("allowedComputers")
        button_current_computer.setStyleSheet(f"""{get_default_config_button_style(self._globalConfiguration.highlightColor)}""")

        # Add widgets to the grid
        grid_layout.addWidget(label_language, 0, 0)
        grid_layout.addWidget(combo_language, 0, 1)

        grid_layout.addWidget(label_alert_color, 1, 0)
        grid_layout.addWidget(input_alert_color, 1, 1)

        grid_layout.addWidget(label_highlight_color, 2, 0)
        grid_layout.addWidget(input_highlight_color, 2, 1)

        grid_layout.addWidget(label_protection_level, 3, 0)
        grid_layout.addWidget(combo_protection_level, 3, 1)

        grid_layout.addWidget(label_current_guid, 4, 0)
        grid_layout.addWidget(button_current_computer, 4, 1)

        combo_language.currentIndexChanged.connect(self.__on_input_change)
        input_alert_color.textChanged.connect(self.__on_input_change)
        input_highlight_color.textChanged.connect(self.__on_input_change)
        combo_protection_level.currentIndexChanged.connect(self.__on_input_change)
        button_current_computer.clicked.connect(self.__on_guid_button_press)

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

    def __on_guid_button_press(self, event):
        # if scryptum.machine_key_exists():
        #     return
        scryptum.create_machine_key(self._sosConfiguration.configurationPassword)

    def __on_alert_color_clicked(self, event):
        picked_color = getColor(hex2rgb(self._globalConfiguration.alertColor))
        print(rgb2hex(picked_color))

        self._globalViewModel.update_model("alertColor",
                                           rgb2hex(picked_color))

    def __on_highlight_color_clicked(self, event):
        picked_color = getColor(hex2rgb(self._globalConfiguration.highlightColor))
        print(rgb2hex(picked_color))

        self._globalViewModel.update_model("highlightColor",
                                           rgb2hex(picked_color))
