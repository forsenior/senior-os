import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QApplication, QMainWindow, \
    QSpacerItem, QSizePolicy

from sconf.ui.styles.global_style_sheets import get_main_window_style, get_default_menu_button_style, \
    get_active_menu_button_style
from sconf.ui.view.credits_view import CreditsView
from sconf.ui.view.global_settings_view import GlobalSettingsView
from sconf.ui.view.smail_settings_view import MailSettingsView
from sconf.ui.view.sweb_settings_view import WebSettingsView


class MainWindow(QMainWindow):
    _configurationFolder: str

    def __init__(self, screen: QApplication,  configurationProvider,
                 configurationWriter,
                 configurationFolder: str):
        super().__init__()

        self._configurationProvider = configurationProvider
        self._configurationWriter = configurationWriter
        self._configurationFolder = configurationFolder

        self.global_configuration = configurationProvider.get_global_configuration()
        sweb_configuration = configurationProvider.get_sweb_configuration()
        smail_configuration = configurationProvider.get_smail_configuration()
        sos_configuration = configurationProvider.get_main_configuration()

        # Set main window properties
        self.setWindowTitle("SCONF")
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

        # Menu layout
        self.menu_layout = QHBoxLayout(container)
        self.menu_layout.setContentsMargins(10, 12, 10, 1)
        self.menu_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))  # Consistent spacing between buttons

        # Creating the menu buttons
        self.menu_buttons = {
            "Credits": QPushButton("Credits"),
            "X": QPushButton(""),
            "Global": QPushButton("Global"),
            "Web": QPushButton("Web"),
            "Mail": QPushButton("Mail")
        }

        # Set up each button with proper sizing and styling
        for name, button in self.menu_buttons.items():
            button.setFixedSize(244, 107)  # Updated size to match Figma
            if name == "X":
                pixmap_icon = QPixmap("/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/exit.png").scaled(40, 40, Qt.KeepAspectRatio,
                                                                        Qt.SmoothTransformation)
                button.setIconSize(QSize(40, 40))
                button.setIcon(QIcon(pixmap_icon))
            self.menu_layout.addWidget(button, alignment=Qt.AlignCenter)

        self.menu_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.main_layout.addLayout(self.menu_layout)

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
        self.credit_views = CreditsView()
        self.global_view = GlobalSettingsView(self.global_configuration, sweb_configuration, smail_configuration, sos_configuration=sos_configuration)
        self.web_view = WebSettingsView(sweb_configuration, configurationFolder, self.global_configuration.highlightColor)
        self.mail_view = MailSettingsView(smail_configuration, self.global_configuration, configurationFolder, self.global_configuration.highlightColor)

        # Adding views to the stacked widget
        self.stacked_widget.addWidget(self.credit_views) # Index 0
        self.stacked_widget.addWidget(self.global_view)  # Index 1
        self.stacked_widget.addWidget(self.web_view)  # Index 2
        self.stacked_widget.addWidget(self.mail_view)  # Index 3

        # Adding the stacked widget to the main layout
        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.addStretch()  # Adds space at the bottom

        # Connecting menu buttons to their respective actions
        self.menu_buttons["Credits"].clicked.connect(self.show_credits_view)
        self.menu_buttons["X"].clicked.connect(self.terminate_shelp)
        self.menu_buttons["Global"].clicked.connect(self.show_global_view)
        self.menu_buttons["Web"].clicked.connect(self.show_web_view)
        self.menu_buttons["Mail"].clicked.connect(self.show_mail_view)

        screenGeometry = screen.geometry()
        container.move(
             (screenGeometry.width() - container.width()) // 2,
             (screenGeometry.height() - container.height()) // 2
        )

        # Set initial active view
        self.show_global_view()

    def show_credits_view(self):
        self.menu_buttons["Credits"].setStyleSheet(get_active_menu_button_style(self.global_configuration.highlightColor))
        self.menu_buttons["Global"].setStyleSheet(get_default_menu_button_style(self.global_configuration.highlightColor))
        self.menu_buttons["Web"].setStyleSheet(get_default_menu_button_style(self.global_configuration.highlightColor))
        self.menu_buttons["Mail"].setStyleSheet(get_default_menu_button_style(self.global_configuration.highlightColor))
        self.stacked_widget.setCurrentIndex(0)

    def terminate_shelp(self):
        self._configurationWriter.update_configuration(
            configuration=self._configurationProvider.get_main_configuration()
        )
        sys.exit(0)

    def show_global_view(self):
        self.menu_buttons["Credits"].setStyleSheet(get_default_menu_button_style(self.global_configuration.highlightColor))
        self.menu_buttons["Global"].setStyleSheet(get_active_menu_button_style(self.global_configuration.highlightColor))
        self.menu_buttons["Web"].setStyleSheet(get_default_menu_button_style(self.global_configuration.highlightColor))
        self.menu_buttons["Mail"].setStyleSheet(get_default_menu_button_style(self.global_configuration.highlightColor))
        self.stacked_widget.setCurrentIndex(1)

    def show_web_view(self):
        self.menu_buttons["Credits"].setStyleSheet(get_default_menu_button_style(self.global_configuration.highlightColor))
        self.menu_buttons["Global"].setStyleSheet(get_default_menu_button_style(self.global_configuration.highlightColor))
        self.menu_buttons["Web"].setStyleSheet(get_active_menu_button_style(self.global_configuration.highlightColor))
        self.menu_buttons["Mail"].setStyleSheet(get_default_menu_button_style(self.global_configuration.highlightColor))
        self.stacked_widget.setCurrentIndex(2)

    def show_mail_view(self):
        self.menu_buttons["Credits"].setStyleSheet(get_default_menu_button_style(self.global_configuration.highlightColor))
        self.menu_buttons["Global"].setStyleSheet(get_default_menu_button_style(self.global_configuration.highlightColor))
        self.menu_buttons["Web"].setStyleSheet(get_default_menu_button_style(self.global_configuration.highlightColor))
        self.menu_buttons["Mail"].setStyleSheet(get_active_menu_button_style(self.global_configuration.highlightColor))
        self.stacked_widget.setCurrentIndex(3)
