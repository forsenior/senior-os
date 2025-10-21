import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QApplication, QMainWindow, \
    QSpacerItem, QSizePolicy

from sconf.ui.styles.global_style_sheets import get_main_window_style, get_default_menu_button_style, \
    get_active_menu_button_style
import sconf.configuration.configuration_writer as configurationWriter
import sconf.configuration.configuration_provider as configurationProvider
from smail.visual_settings_view import VisualSettingsView
from smail.security_settings_view import SecuritySettingsView
from smail.smail_settings_view import MailSettingsView
from smail.layout import first_frame

class MainWindow(QMainWindow):
    _configurationFolder: str

    def __init__(self, screen: QApplication,  configurationProvider,
                 configurationWriter,
                 configurationFolder: str):
        super().__init__()

        

        self.global_configuration = configurationProvider.get_global_configuration()
        smail_configuration = configurationProvider.get_smail_configuration()
        sos_configuration = configurationProvider.get_main_configuration()

        # Set main window properties
        self.setWindowTitle("MainMail")
        self.setMinimumSize(1280, 800)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: #FFFFFF;")

        # Create fixed-size container that will hold everything
        container = QWidget(self)
        container.setFixedSize(1280, 800)  # Fixed size to match Figma
        container.setStyleSheet(f"""
                    {get_main_window_style()}
                    {get_default_menu_button_style(self.global_configuration.highlightColor)}
                    border: 2px solid #000000;
                    border-radius: 8px;
                    margin: 40px;
                """)

        # Main layout inside the container
        self.main_layout = QVBoxLayout(container)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(16)

        # Stack for holding multiple views (screens)
        self.stacked_widget = QStackedWidget(container)
        self.stacked_widget.setStyleSheet("""
                    QStackedWidget {
                        background-color: #FFFFFF;
                        border: 2px solid #000000;
                        border-radius: 8px;
                        padding: 16px;
                        position: relative
                    }
                """)

        # Creating views for different sections
        self.first_frame = first_frame(self, configurationProvider, self.stacked_widget)
        self.security_view = SecuritySettingsView(self.global_configuration, smail_configuration, sos_configuration=sos_configuration)
        self.visual_view = VisualSettingsView(self.global_configuration, sos_configuration=sos_configuration)
        self.mail_view = MailSettingsView(smail_configuration, self.global_configuration, configurationFolder, self.global_configuration.highlightColor)

        # Adding views to the stacked widget
        self.stacked_widget.addWidget(self.first_frame) # Index 0
        self.stacked_widget.addWidget(self.security_view)  # Index 1
        self.stacked_widget.addWidget(self.visual_view)  # Index 2
        self.stacked_widget.addWidget(self.mail_view)  # Index 3

        # Adding the stacked widget to the main layout
        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.addStretch()  # Adds space at the bottom

        screenGeometry = screen.geometry()
        container.move(
             (screenGeometry.width() - container.width()) // 2,
             (screenGeometry.height() - container.height()) // 2
        )

        # Set initial active view
        self.first_frame()

    def terminate_shelp(self):
        self._configurationWriter.update_configuration(
            configuration=self._configurationProvider.get_main_configuration()
        )
        self.stacked_widget.setCurrentIndex(0)

    def show_global_view(self):
       
        self.stacked_widget.setCurrentIndex(1)

    def show_security_view(self):

        self.stacked_widget.setCurrentIndex(2)

    def show_mail_view(self):

        self.stacked_widget.setCurrentIndex(3)
