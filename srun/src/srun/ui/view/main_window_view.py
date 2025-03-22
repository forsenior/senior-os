import os.path
import scryptum

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout, QDialog, QLabel
from srun.data.executables import SosExecutables
from srun.ui.dialog.password_dialog import PasswordPopup
from srun.ui.styles.srun_style_sheets import get_default_start_button_style, get_default_center_widget_style, get_transparent_label_style
from sconf.configuration.configuration_provider import ConfigurationProvider
from sconf.configuration.configuration_writer import ConfigurationWriter


class MainWindowView(QWidget):
    __executables: SosExecutables
    _is_initial_startup: bool
    _machine_key_state: bool

    def __init__(self, data_provider: ConfigurationProvider,
                 data_writer: ConfigurationWriter):
        super().__init__()
        self.main_configuration = data_provider.get_main_configuration()
        self.global_configuration = data_provider.get_global_configuration()
        self.data_writer = data_writer

        self._is_initial_startup = True if (self.main_configuration.configurationPassword == ""
                                            and self.main_configuration.initialStartUp) else False
        self._machine_key_state = scryptum.machine_key_exists()

        self.timer = QTimer()
        self.timer.setInterval(30)
        self.timer.timeout.connect(self.__update_progress)
        self.hold_duration = 3000
        self.elapsed_time = 0

        self.__executables = SosExecutables()

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

        label_exit = QLabel("Press and hold to shutdown")
        label_exit.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        label_exit.setStyleSheet(get_transparent_label_style())

        # Create buttons
        button_exit = QPushButton()
        button_smail = QPushButton("SMAIL")
        button_sweb = QPushButton("SWEB")
        button_sconf = QPushButton("SCONF")

        button_exit.setStyleSheet(get_default_start_button_style(self.global_configuration.highlightColor))
        button_smail.setStyleSheet(get_default_start_button_style(self.global_configuration.highlightColor))
        button_sweb.setStyleSheet(get_default_start_button_style(self.global_configuration.highlightColor))
        button_sconf.setStyleSheet(get_default_start_button_style(self.global_configuration.highlightColor))

        pixmap_icon = QPixmap(r"/run/archiso/airootfs/usr/lib/python3.13/site-packages/icons/exit.png").scaled(100, 100)
        button_exit.setIconSize(QSize(100, 100))
        button_exit.setIcon(QIcon(pixmap_icon))

        grid_layout.addWidget(button_smail, 0, 0)
        grid_layout.addWidget(button_sweb, 0, 1)
        grid_layout.addWidget(button_sconf, 1, 0)
        grid_layout.addWidget(button_exit, 1, 1)
        grid_layout.addWidget(label_exit, 1, 1)

        button_exit.pressed.connect(self.__start_timer)
        button_exit.released.connect(self.__stop_timer)

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

        if not self._machine_key_state or self._is_initial_startup:
            self.__handle_sconf_clicked()

    def __start_timer(self):
        self.elapsed_time = 0
        self.timer.start()

    def __stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()

    def __update_progress(self):
        self.elapsed_time += self.timer.interval()
        # self.progress_bar.setValue(self.elapsed_time)

        if self.elapsed_time >= self.hold_duration:
            self.timer.stop()
            self.__handle_exit_timeout()

    def __handle_exit_timeout(self):
        print("Timeout elapsed shutting down the system")
        os.system(f"poweroff")

    def __handle_smail_clicked(self):
        os.system(f"{self.__executables.smail}")

    def __handle_sweb_clicked(self):
        os.system(f"{self.__executables.sweb}")

    def __handle_sconf_clicked(self):
        password_dialog = PasswordPopup(password=self.main_configuration.configurationPassword,
                                        initial_start_up=self.main_configuration.initialStartUp)

        match password_dialog.exec_():
            case QDialog.Accepted:
                if self._is_initial_startup and scryptum.machine_key_exists():
                    self.main_configuration.configurationPassword = password_dialog.get_confirmed_password()
                    self.main_configuration.initialStartUp = False
                    scryptum.create_master_key(self.main_configuration.configurationPassword)
                    scryptum.create_machine_key(self.main_configuration.configurationPassword)
                    self.data_writer.update_configuration(self.main_configuration)
                os.system(f"{self.__executables.sconf}")
                return
            case QDialog.Rejected:
                print("Given password is either empty or incorrect. Please try again.")
                return
            case _:
                print("Password setup canceled.")
                return
