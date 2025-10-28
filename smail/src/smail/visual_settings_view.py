
from PyQt5.QtCore import pyqtSlot, QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QLineEdit, QGridLayout, QPushButton, QVBoxLayout, QSpacerItem, \
QSizePolicy, QFrame, QComboBox

from PyQt5.QtWidgets import QColorDialog

from smail import style
from sconf.configuration.models.global_configuration import GlobalConfiguration
from sconf.configuration.models.sos_configuration import SOSConfiguration
from sconf.configuration.models.smail_configuration import SmailConfiguration
from sconf.ui.convertors.value_convertors import StringValueConvertors
from sconf.ui.styles.global_style_sheets import get_default_label_style, get_default_input_box_style, \
    get_default_dropdown_style, get_default_config_button_style
from sconf.ui.view_models.global_settings_view_model import GlobalViewModel



class VisualSettingsView(QWidget):
    _globalViewModel: GlobalViewModel
    _globalConfiguration: GlobalConfiguration
    _sosConfiguration: SOSConfiguration

    def __init__(self, global_configuration: GlobalConfiguration,
                 smail_configuration: SmailConfiguration,
                 sos_configuration: SOSConfiguration,
                 data_provider, configuration_writer, stacked_widget
                 ):
    
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.data_provider = data_provider
        self.configuration_writer = configuration_writer
        self.stacked_widget = stacked_widget
        # Menu layout
        self.button_frame = QFrame(self)
        self.button_frame.setStyleSheet(style.get_button_frame_style())
        self.button_frame.setFrameShape(QFrame.StyledPanel)
        self.button_frame.setFixedHeight(130)
        self.button_layout = QHBoxLayout(self.button_frame)
        spacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button_layout.addItem(spacer_left)

        # Creating the menu buttons
        self.menu_buttons = {
            "Menu1": QPushButton("Menu1"),
            "X": QPushButton(""),
            "Security": QPushButton("Security"),
            "Visual": QPushButton("Visual"),
            "Mail": QPushButton("Mail")
        }

        # Set up each button with proper sizing and styling
        for name, button in self.menu_buttons.items():
            button.setFixedSize(244, 107) # Updated size to match Figma
            if name == "X":
                pixmap_icon = QPixmap("/home/vboxuser/senior-os/sconf/icons/exit.png").scaled(40, 40, Qt.KeepAspectRatio,
                                                                        Qt.SmoothTransformation)
                button.setIconSize(QSize(40, 40))
                button.setIcon(QIcon(pixmap_icon))
            self.button_layout.addWidget(button, alignment=Qt.AlignCenter)
            button.setStyleSheet(style.get_button_style(self.data_provider))

        self.button_layout.setSpacing(10)
        self.button_layout.addItem(spacer_right)
        self.button_frame.setStyleSheet(style.get_button_frame_style())
        self.main_layout.addWidget(self.button_frame)

        # Create layout for labels and input fields

        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        self._globalConfiguration = global_configuration
        
        self._sosConfiguration = sos_configuration
        self._globalViewModel = GlobalViewModel(global_configuration,  smail_configuration)

        # Labels
        label_alert_color = QLabel("Alert color (in hex)")
        label_highlight_color = QLabel("Highlight color (in hex)")


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

        # Add widgets to the grid

        grid_layout.addWidget(label_alert_color, 0, 0)
        grid_layout.addWidget(input_alert_color, 0, 1)

        grid_layout.addWidget(label_highlight_color, 1, 0)
        grid_layout.addWidget(input_highlight_color, 1, 1)

        input_alert_color.textChanged.connect(self.__on_input_change)
        input_highlight_color.textChanged.connect(self.__on_input_change)

        # Set widget layout

        self.main_layout.addLayout(grid_layout)
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

        # Apply styling
        self.setStyleSheet(f"""
                            {get_default_label_style()}
                            {get_default_input_box_style()}
                            {get_default_dropdown_style()}
                        """)
        self.button_frame.setStyleSheet(style.get_button_frame_style())
        self.menu_buttons["Menu1"].setStyleSheet(style.get_button_style(self.data_provider))
        self.menu_buttons["X"].setStyleSheet(style.get_button_style(self.data_provider))
        self.menu_buttons["Security"].setStyleSheet(style.get_button_style(self.data_provider))
        self.menu_buttons["Visual"].setStyleSheet(style.get_button_style(self.data_provider))
        self.menu_buttons["Mail"].setStyleSheet(style.get_button_style(self.data_provider))

        self.menu_buttons["X"].clicked.connect(self.terminate_shelp)
        self.menu_buttons["Menu1"].clicked.connect(self.terminate_shelp)
        self.menu_buttons["Security"].clicked.connect(self.show_security_view)
        self.menu_buttons["Visual"].clicked.connect(self.show_visual_view)
        self.menu_buttons["Mail"].clicked.connect(self.show_mail_view)


    def terminate_shelp(self):
        self.configuration_writer.update_configuration(
            configuration=self.data_provider.get_main_configuration()
        )
        self.stacked_widget.setCurrentIndex(0)
    def show_security_view(self):
        self.stacked_widget.setCurrentIndex(1)
    def show_visual_view(self):
        self.stacked_widget.setCurrentIndex(2)
    def show_mail_view(self):
        self.stacked_widget.setCurrentIndex(3)

    @pyqtSlot()
    def __on_input_change(self):
        sender = self.sender()

        if sender.objectName() == "language" and isinstance(sender, QComboBox):
            print(StringValueConvertors.language_to_country_code(sender.currentText()))
            self._globalViewModel.update_model(sender.objectName(),
                                               StringValueConvertors.language_to_country_code(sender.currentText()))


    def __on_alert_color_clicked(self, event):
        picked_color = QColorDialog.getColor()
        print(picked_color.name())

        self._globalViewModel.update_model("alertColor",
                                           (picked_color.name()))

    def __on_highlight_color_clicked(self, event):
        picked_color = QColorDialog.getColor()
        print(picked_color.name())
        self._globalViewModel.update_model("highlightColor",
                                           (picked_color.name()))
    
    