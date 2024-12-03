import os.path
import sys

from typing import List

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout, QDialog

from srun.data.executables import SosExecutables
from srun.ui.dialog.password_dialog import PasswordPopup
from srun.ui.styles.srun_style_sheets import get_default_start_button_style, get_default_center_widget_style
from sconf.configuration.configuration_provider import ConfigurationProvider
from sconf.configuration.configuration_writer import ConfigurationWriter


class MainWindowView(QWidget):
    __working_directory: str
    __srun_free_path: str
    __poetry_run_command: str = "poetry run python"
    __executables: SosExecutables

    def __init__(self, start_objects: List[str], data_provider: ConfigurationProvider,
                 data_writer: ConfigurationWriter):
        super().__init__()

        self.__working_directory = os.getcwd()
        self.__srun_free_path = self.__working_directory.split('srun')[0]
        self.__executables = SosExecutables()

        self.main_configuration = data_provider.get_main_configuration()
        self.data_writer = data_writer

        self.setWindowTitle("SRUN")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()

        # Set main background style
        self.setStyleSheet(f"""
                    background-color: #FFFFFF;
                """)

        # Main container layout to center the widget
        main_layout = QVBoxLayout(self)

        # Central container for buttons with fixed size
        central_widget = QWidget()
        central_widget.setStyleSheet(get_default_center_widget_style())

        # Grid layout for buttons within the central widget
        grid_layout = QGridLayout(central_widget)

        # Create buttons
        button_exit = QPushButton("")
        button_smail = QPushButton("MAIL")
        button_sweb = QPushButton("WEB")
        button_sconf = QPushButton("CONF")

        button_exit.setStyleSheet(get_default_start_button_style())
        button_smail.setStyleSheet(get_default_start_button_style())
        button_sweb.setStyleSheet(get_default_start_button_style())
        button_sconf.setStyleSheet(get_default_start_button_style())

        pixmap_icon = QPixmap(r"../sconf/icons/exit.png").scaled(100, 100)
        button_exit.setIconSize(QSize(100, 100))
        button_exit.setIcon(QIcon(pixmap_icon))

        grid_layout.addWidget(button_smail, 0, 0)
        grid_layout.addWidget(button_sweb, 0, 1)
        grid_layout.addWidget(button_sconf, 1, 0)
        grid_layout.addWidget(button_exit, 1, 1)

        button_exit.clicked.connect(self.__handle_exit_clicked)
        button_smail.clicked.connect(self.__handle_smail_clicked)
        button_sweb.clicked.connect(self.__handle_sweb_clicked)
        button_sconf.clicked.connect(self.__handle_sconf_clicked)

        # Center the central widget in the full-screen layout
        main_layout.addStretch(1)  # Add space above the central widget
        h_layout = QHBoxLayout()
        h_layout.addStretch(1)  # Add space to the left
        h_layout.addWidget(central_widget)
        h_layout.addStretch(1)  # Add space to the right
        main_layout.addLayout(h_layout)
        main_layout.addStretch(1)  # Add space below the central widget

    def __handle_exit_clicked(self):
        sys.exit(0)

    def __handle_smail_clicked(self):
        sweb_directory = os.path.join(self.__srun_free_path, 'smail')

        os.chdir(sweb_directory)

        os.system(f"{self.__poetry_run_command} {self.__executables.smail}")
        os.chdir(self.__working_directory)
        print(os.getcwd())

    def __handle_sweb_clicked(self):
        sweb_directory = os.path.join(self.__srun_free_path, 'sweb')

        os.chdir(sweb_directory)

        os.system(f"{self.__poetry_run_command} {self.__executables.sweb}")
        os.chdir(self.__working_directory)
        print(os.getcwd())

    def __handle_sconf_clicked(self):
        sconf_directory = os.path.join(self.__srun_free_path, 'sconf')
        password_dialog = PasswordPopup(password=self.main_configuration.configurationPassword,
                                        initial_start_up=self.main_configuration.initialStartUp)

        is_initial_start_up = True if (self.main_configuration.configurationPassword == ""
                                       and self.main_configuration.initialStartUp) else False

        if password_dialog.exec_() == QDialog.Accepted:
            os.chdir(sconf_directory)
            if is_initial_start_up:
                self.main_configuration.configurationPassword = password_dialog.get_confirmed_password()
                self.main_configuration.initialStartUp = False
                self.data_writer.update_configuration(self.main_configuration)

            os.system(f"{self.__poetry_run_command} {self.__executables.sconf}")
            os.chdir(self.__working_directory)
        else:
            # Handle the case where the dialog was canceled if needed
            print("Password setup canceled.")
